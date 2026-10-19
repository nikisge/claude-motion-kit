// hf3d: Premium-Produkt-3D für HyperFrames (Three.js r181, alles lokal).
// Seek-sicher nach hyperframes-animation/adapters/three.md: jedes Bild ist eine reine Funktion von t.
// Kein requestAnimationFrame, kein Date.now/performance.now, Zufall nur über rng(seed).
// Doku + Fallstricke: README.md (gleicher Ordner)
import * as THREE from "three";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";
import { TextGeometry } from "three/addons/geometries/TextGeometry.js";
import { SVGLoader } from "three/addons/loaders/SVGLoader.js";
import { Font } from "three/addons/loaders/FontLoader.js";
import { TTFLoader } from "three/addons/loaders/TTFLoader.js";
import { MeshSurfaceSampler } from "three/addons/math/MeshSurfaceSampler.js";
import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";
import { FullScreenQuad } from "three/addons/postprocessing/Pass.js";
import * as BufferGeometryUtils from "three/addons/utils/BufferGeometryUtils.js";

export { THREE, BufferGeometryUtils };

// ───────────────────────── Mathe, Easing, Zufall ─────────────────────────
export const clamp01 = (x) => Math.min(1, Math.max(0, x));
export const lerp = (a, b, u) => a + (b - a) * u;
export const ease = {
  linear: (u) => u,
  inOut: (u) => (u < 0.5 ? 4 * u * u * u : 1 - Math.pow(-2 * u + 2, 3) / 2), // Kamerafahrt
  inOut2: (u) => (u < 0.5 ? 2 * u * u : 1 - Math.pow(-2 * u + 2, 2) / 2),
  sine: (u) => -(Math.cos(Math.PI * u) - 1) / 2,
  out: (u) => 1 - Math.pow(1 - u, 3),
  in: (u) => u * u * u,
  expoOut: (u) => (u >= 1 ? 1 : 1 - Math.pow(2, -10 * u)),
  expoIn: (u) => (u <= 0 ? 0 : Math.pow(2, 10 * u - 10)),
  expoInOut: (u) => (u <= 0 ? 0 : u >= 1 ? 1 : u < 0.5 ? Math.pow(2, 20 * u - 10) / 2 : (2 - Math.pow(2, -20 * u + 10)) / 2),
  backOut: (u, s = 1.6) => 1 + (s + 1) * Math.pow(u - 1, 3) + s * Math.pow(u - 1, 2),
  // Feder (Gewicht, 4–8 % Überschwinger): gedämpfte Schwingung, endet exakt bei 1
  spring: (u, k = 7, d = 5.5) => (u >= 1 ? 1 : 1 - Math.exp(-d * u) * Math.cos(k * u) * (1 - u)),
};
/** Anteil 0..1 von t im Fenster [a,b], mit Easing. */
export const seg = (t, a, b, fn = ease.linear) => fn(clamp01((t - a) / (b - a)));
export function rng(seed = 1) {
  let a = seed >>> 0;
  return function () {
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
// Glattes 1D-Rauschen (für Handkamera, Drift), deterministisch
function hash1(n) { const s = Math.sin(n * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); }
export function noise1(x, seed = 0) {
  const i = Math.floor(x), f = x - i, u = f * f * (3 - 2 * f);
  return lerp(hash1(i + seed * 17.13), hash1(i + 1 + seed * 17.13), u) * 2 - 1;
}
const v3 = (a) => (a instanceof THREE.Vector3 ? a.clone() : Array.isArray(a) ? new THREE.Vector3(a[0], a[1], a[2]) : new THREE.Vector3());
const col = (c) => (c instanceof THREE.Color ? c : new THREE.Color(c));

// ───────────────────────── Prozedurale Texturen (geseedet) ─────────────────────────
function dataTex(w, h, fill, { repeat = [1, 1], srgb = false } = {}) {
  const data = new Uint8Array(w * h * 4);
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    const v = fill(x, y); const i = (y * w + x) * 4;
    data[i] = v[0]; data[i + 1] = v[1]; data[i + 2] = v[2]; data[i + 3] = 255;
  }
  const tex = new THREE.DataTexture(data, w, h, THREE.RGBAFormat);
  tex.wrapS = tex.wrapT = THREE.RepeatWrapping; tex.repeat.set(repeat[0], repeat[1]);
  tex.magFilter = THREE.LinearFilter; tex.minFilter = THREE.LinearMipmapLinearFilter; tex.generateMipmaps = true;
  tex.anisotropy = 8; if (srgb) tex.colorSpace = THREE.SRGBColorSpace;
  tex.needsUpdate = true; return tex;
}
/** Gebürstete Rillen: Zeilenrauschen, entlang x gestreckt. Für roughnessMap + bumpMap. */
export function brushedTexture({ seed = 7, size = 512, strength = 0.5, repeat = [1, 1] } = {}) {
  const r = rng(seed); const rows = new Float32Array(size);
  for (let y = 0; y < size; y++) rows[y] = r();
  const lowA = Array.from({ length: 9 }, () => r());
  return dataTex(size, size, (x, y) => {
    const fine = rows[y] * 0.65 + rows[(y + 1) % size] * 0.35;
    const low = lerp(lowA[Math.floor((x / size) * 8)], lowA[Math.floor((x / size) * 8) + 1], ((x / size) * 8) % 1);
    const v = 128 + (fine - 0.5) * 255 * strength + (low - 0.5) * 30;
    const c = Math.max(0, Math.min(255, v)); return [c, c, c];
  }, { repeat });
}
/** Feine Körnung für Soft-Touch / Keramik (Mikro-Rauheit). */
export function grainTexture({ seed = 3, size = 256, strength = 0.25, repeat = [4, 4] } = {}) {
  const r = rng(seed);
  return dataTex(size, size, () => { const c = 128 + (r() - 0.5) * 255 * strength; return [c, c, c]; }, { repeat });
}

// ───────────────────────── Material-Presets ─────────────────────────
// Alle physikalisch (MeshPhysicalMaterial) und auf eine Umgebung (env) angewiesen: ohne env wirkt Metall schwarz.
export const mat = {
  brushedMetal({ color = "#c9ccd2", roughness = 0.28, anisotropy = 0.8, anisotropyRotation = 0, seed = 7, repeat = [1, 4], bump = 0.03, strength = 0.3 } = {}) {
    const tex = brushedTexture({ seed, repeat, strength });
    return new THREE.MeshPhysicalMaterial({ color: col(color), metalness: 1, roughness, roughnessMap: tex,
      bumpMap: tex, bumpScale: bump, anisotropy, anisotropyRotation, clearcoat: 0.0 });
  },
  polishedMetal({ color = "#e6e7ea", roughness = 0.06 } = {}) {
    return new THREE.MeshPhysicalMaterial({ color: col(color), metalness: 1, roughness });
  },
  /** Glas: teuer (zusätzlicher Transmission-Durchgang je Bild). thickness in Welt-Einheiten. */
  glass({ tint = "#ffffff", roughness = 0.04, thickness = 0.4, ior = 1.5, dispersion = 0.0, attenuationColor = null, attenuationDistance = 2, opacity = 1 } = {}) {
    const m = new THREE.MeshPhysicalMaterial({ color: col(tint), metalness: 0, roughness, transmission: 1, thickness, ior,
      dispersion, specularIntensity: 1, envMapIntensity: 1.2, transparent: opacity < 1, opacity });
    if (attenuationColor) { m.attenuationColor = col(attenuationColor); m.attenuationDistance = attenuationDistance; }
    return m;
  },
  softTouch({ color = "#2a2b2f", roughness = 0.62, sheen = 0.35, sheenColor = "#ffffff", seed = 3 } = {}) {
    return new THREE.MeshPhysicalMaterial({ color: col(color), metalness: 0, roughness, sheen, sheenRoughness: 0.8,
      sheenColor: col(sheenColor), roughnessMap: grainTexture({ seed, strength: 0.18 }) });
  },
  ceramic({ color = "#f2efe9", roughness = 0.38, clearcoat = 0.85, clearcoatRoughness = 0.12 } = {}) {
    return new THREE.MeshPhysicalMaterial({ color: col(color), metalness: 0, roughness, clearcoat, clearcoatRoughness });
  },
  glossyPlastic({ color = "#ff5a1f", roughness = 0.28, clearcoat = 1, clearcoatRoughness = 0.06 } = {}) {
    return new THREE.MeshPhysicalMaterial({ color: col(color), metalness: 0, roughness, clearcoat, clearcoatRoughness });
  },
  /** Leuchtet; intensity > 1 erzeugt Bloom (Schwelle threshold in post.bloom). */
  emissive({ color = "#ff7a2f", intensity = 4, base = "#111111" } = {}) {
    return new THREE.MeshStandardMaterial({ color: col(base), emissive: col(color), emissiveIntensity: intensity, roughness: 0.5, metalness: 0 });
  },
};

// ───────────────────────── Umgebung + Licht ─────────────────────────
/** Studio-Umgebung: dunkler Raum mit Softboxen (lange Glanzlichter auf Metall/Glas). */
export function studioEnvScene({ tone = "dark", key = 7, strip = 5, warm = "#fff1e2", cool = "#e2ecff", floor, walls } = {}) {
  // tone "bright": helle Hohlkehle (helle Szenen, silbernes Metall), "dark": dunkler Raum (kontrastreiche Glanzkanten)
  floor = floor || (tone === "bright" ? "#d9cfc8" : "#2a2522"); walls = walls || (tone === "bright" ? "#8d8783" : "#151417");
  const s = new THREE.Scene();
  s.add(new THREE.Mesh(new THREE.BoxGeometry(30, 30, 30), new THREE.MeshBasicMaterial({ color: col(walls), side: THREE.BackSide })));
  const panel = (w, h, pos, rot, c, k) => {
    const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ color: col(c).clone().multiplyScalar(k), side: THREE.DoubleSide }));
    m.position.set(...pos); m.rotation.set(...rot); s.add(m);
  };
  panel(12, 6, [-3, 9, 3], [Math.PI / 2.2, 0, 0], warm, key);      // Key-Softbox oben links
  panel(1.6, 14, [10, 1, -1], [0, -Math.PI / 2, 0], cool, strip);  // Streifen rechts (Rim)
  panel(1.6, 14, [-10, 0, 2], [0, Math.PI / 2, 0], warm, strip * 0.7); // Streifen links
  panel(16, 1.2, [0, -1.5, -12], [0, 0, 0], cool, 1.6);             // Horizont-Linie hinten
  panel(20, 20, [0, -6, 0], [-Math.PI / 2, 0, 0], floor, 1);        // Boden-Abstrahlung
  return s;
}

/** Key/Rim/Fill. Key wirft weiche Schatten. Richtungen = Position, Licht zeigt auf target. */
export function studioLights(scene, {
  key = { pos: [-4, 7, 5], color: "#fff3e6", intensity: 2.4 },
  rim = { pos: [5, 3, -6], color: "#d6e4ff", intensity: 2.0 },
  fill = { pos: [3, 1, 7], color: "#ffe8d6", intensity: 0.5 },
  target = [0, 0, 0], shadow = { size: 2048, area: 3, near: 0.5, far: 30, bias: -0.0004, normalBias: 0.02, radius: 4 },
} = {}) {
  const mk = (o, cast) => {
    const l = new THREE.DirectionalLight(col(o.color), o.intensity); l.position.set(...o.pos);
    l.target.position.set(...target); scene.add(l, l.target);
    if (cast && shadow) {
      l.castShadow = true; l.shadow.mapSize.set(shadow.size, shadow.size);
      const c = l.shadow.camera; c.left = c.bottom = -shadow.area; c.right = c.top = shadow.area; c.near = shadow.near; c.far = shadow.far;
      l.shadow.bias = shadow.bias; l.shadow.normalBias = shadow.normalBias; l.shadow.radius = shadow.radius;
    }
    return l;
  };
  return { key: key && mk(key, true), rim: rim && mk(rim, false), fill: fill && mk(fill, false) };
}

// ───────────────────────── Hintergrund (Verlauf statt Schwarz) ─────────────────────────
/** Bildschirmfester Verlauf als Szenen-Objekt (wird so auch im Glas gebrochen). Farben sRGB-Hex. */
export function gradientBackground({ top = "#f6efe9", bottom = "#e9c3a8", glow = "#ffffff", glowPos = [0.62, 0.42], glowSize = 0.55, glowStrength = 0.6,
  glow2 = null, glow2Pos = [0.15, 0.85], glow2Size = 0.5, glow2Strength = 0.5, angle = 0 } = {}) {
  const lin = (c) => col(c).clone(); // THREE.Color hält linear (ColorManagement an)
  const u = {
    uTop: { value: lin(top) }, uBottom: { value: lin(bottom) }, uGlow: { value: lin(glow) }, uGlowPos: { value: new THREE.Vector2(...glowPos) },
    uGlowSize: { value: glowSize }, uGlowStrength: { value: glowStrength },
    uGlow2: { value: lin(glow2 || "#000000") }, uGlow2Pos: { value: new THREE.Vector2(...glow2Pos) }, uGlow2Size: { value: glow2Size },
    uGlow2Strength: { value: glow2 ? glow2Strength : 0 }, uAngle: { value: angle }, uAspect: { value: 16 / 9 },
  };
  const m = new THREE.ShaderMaterial({
    uniforms: u, depthTest: false, depthWrite: false, toneMapped: false,
    vertexShader: `varying vec2 vUv; void main(){ vUv = uv; gl_Position = vec4(position.xy, 1.0, 1.0); }`,
    fragmentShader: `varying vec2 vUv; uniform vec3 uTop,uBottom,uGlow,uGlow2; uniform vec2 uGlowPos,uGlow2Pos;
      uniform float uGlowSize,uGlowStrength,uGlow2Size,uGlow2Strength,uAngle,uAspect;
      void main(){
        vec2 c = vUv - 0.5; float ca = cos(uAngle), sa = sin(uAngle);
        float g = clamp((ca*c.y - sa*c.x) + 0.5, 0.0, 1.0); g = g*g*(3.0-2.0*g);
        vec3 col = mix(uBottom, uTop, g);
        vec2 d1 = (vUv - uGlowPos) * vec2(uAspect, 1.0); col += uGlow * uGlowStrength * exp(-dot(d1,d1)/(uGlowSize*uGlowSize));
        vec2 d2 = (vUv - uGlow2Pos) * vec2(uAspect, 1.0); col += uGlow2 * uGlow2Strength * exp(-dot(d2,d2)/(uGlow2Size*uGlow2Size));
        gl_FragColor = vec4(col, 1.0);
      }`,
  });
  const mesh = new THREE.Mesh(new THREE.PlaneGeometry(2, 2), m);
  mesh.frustumCulled = false; mesh.renderOrder = -1e6; mesh.name = "hf3d-background";
  mesh.set = (o) => { for (const k of Object.keys(o)) { const key = "u" + k[0].toUpperCase() + k.slice(1); if (!u[key]) continue;
    if (u[key].value instanceof THREE.Color) u[key].value.set(o[k]); else if (u[key].value instanceof THREE.Vector2) u[key].value.set(...o[k]); else u[key].value = o[k]; } };
  return mesh;
}

/** Weicher Kontaktschatten (radialer Fleck) unter einem Objekt: billig, wirkt sofort „geerdet“. */
export function contactShadow({ size = 3, opacity = 0.45, color = "#2a1a12", softness = 0.55 } = {}) {
  const m = new THREE.ShaderMaterial({
    transparent: true, depthWrite: false, toneMapped: false,
    uniforms: { uC: { value: col(color) }, uO: { value: opacity }, uS: { value: softness } },
    vertexShader: `varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix*modelViewMatrix*vec4(position,1.0); }`,
    fragmentShader: `varying vec2 vUv; uniform vec3 uC; uniform float uO,uS; void main(){ float d = length(vUv-0.5)*2.0;
      float a = (1.0 - smoothstep(1.0 - uS, 1.0, d)) * pow(1.0 - d*0.6, 2.0); gl_FragColor = vec4(uC, a*uO); }`,
  });
  const p = new THREE.Mesh(new THREE.PlaneGeometry(size, size), m); p.rotation.x = -Math.PI / 2; p.renderOrder = -10; return p;
}
/** Boden, der nur Schatten zeigt (Hintergrund-Verlauf bleibt sichtbar). */
export function shadowFloor({ size = 40, opacity = 0.28, y = 0 } = {}) {
  const p = new THREE.Mesh(new THREE.PlaneGeometry(size, size), new THREE.ShadowMaterial({ opacity, depthWrite: true }));
  p.rotation.x = -Math.PI / 2; p.position.y = y; p.receiveShadow = true; return p;
}

// ───────────────────────── Prozedurale Objekte ─────────────────────────
export function roundedBox(w = 1, h = 1, d = 1, radius = 0.08, segments = 4) {
  return new RoundedBoxGeometry(w, h, d, segments, Math.min(radius, Math.min(w, h, d) / 2 - 1e-4));
}
/** Drehteil aus Profil [[r,y],…] (Knopf, Ring, Gehäuse). fillet rundet jede Ecke. */
export function lathe(profile, { segments = 128, fillet = 0, filletSteps = 4 } = {}) {
  let pts = profile.map(([r, y]) => new THREE.Vector2(r, y));
  if (fillet > 0) pts = roundPolyline(pts, fillet, filletSteps);
  const g = new THREE.LatheGeometry(pts, segments); g.computeVertexNormals(); return g;
}
/** Rändelung/Rippen: verschiebt Vertices eines Drehteils radial (cos über den Umfang) im Höhenband [yMin,yMax]. */
export function knurl(geometry, { ribs = 96, depth = 0.012, yMin = -Infinity, yMax = Infinity, rMin = 0, soft = 0.01 } = {}) {
  const p = geometry.attributes.position;
  for (let i = 0; i < p.count; i++) {
    const x = p.getX(i), y = p.getY(i), z = p.getZ(i), r = Math.hypot(x, z);
    if (r < rMin || r < 1e-5) continue;
    const band = Math.min(clamp01((y - yMin) / soft), clamp01((yMax - y) / soft)); if (band <= 0) continue;
    const a = Math.atan2(z, x); const k = 1 - depth * band * (0.5 - 0.5 * Math.cos(ribs * a)) / r;
    p.setXYZ(i, x * k, y, z * k);
  }
  p.needsUpdate = true; geometry.computeVertexNormals(); return geometry;
}
function roundPolyline(pts, r, steps) {
  const out = [pts[0]];
  for (let i = 1; i < pts.length - 1; i++) {
    const p = pts[i], a = pts[i - 1].clone().sub(p), b = pts[i + 1].clone().sub(p);
    const la = a.length(), lb = b.length(); const rr = Math.min(r, la / 2, lb / 2);
    const p0 = p.clone().add(a.normalize().multiplyScalar(rr)), p1 = p.clone().add(b.normalize().multiplyScalar(rr));
    for (let s = 0; s <= steps; s++) { const u = s / steps; const q = p0.clone().multiplyScalar((1 - u) * (1 - u)).add(p.clone().multiplyScalar(2 * u * (1 - u))).add(p1.clone().multiplyScalar(u * u)); out.push(q); }
  }
  out.push(pts[pts.length - 1]); return out;
}
/** Glas-/Licht-Band entlang einer Kurve (wie geschwungene Glasbänder). width quer, twist in Umdrehungen. */
export function ribbon(points, { width = 0.4, segments = 300, twist = 0, closed = false, thickness = 0.02 } = {}) {
  const curve = new THREE.CatmullRomCurve3(points.map(v3), closed, "centripetal");
  const frames = curve.computeFrenetFrames(segments, closed);
  const pos = [], nor = [], uv = [], idx = [];
  for (let i = 0; i <= segments; i++) {
    const u = i / segments, p = curve.getPointAt(u), n = frames.normals[Math.min(i, segments)].clone(), b = frames.binormals[Math.min(i, segments)].clone();
    const a = twist * Math.PI * 2 * u; const side = n.clone().multiplyScalar(Math.cos(a)).add(b.clone().multiplyScalar(Math.sin(a)));
    const up = side.clone().cross(curve.getTangentAt(u)).normalize();
    for (const s of [-1, 1]) for (const f of [-1, 1]) { // 4 Kanten: vorne/hinten
      const q = p.clone().addScaledVector(side, (s * width) / 2).addScaledVector(up, (f * thickness) / 2);
      pos.push(q.x, q.y, q.z); nor.push(up.x * f, up.y * f, up.z * f); uv.push(u, (s + 1) / 2);
    }
  }
  for (let i = 0; i < segments; i++) {
    const o = i * 4, n = o + 4;
    idx.push(o + 1, n + 1, o + 3, n + 1, n + 3, o + 3); // Oberseite (f=+1: Indizes 1,3)
    idx.push(o + 0, o + 2, n + 0, n + 0, o + 2, n + 2); // Unterseite
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute("position", new THREE.Float32BufferAttribute(pos, 3)); g.setAttribute("normal", new THREE.Float32BufferAttribute(nor, 3));
  g.setAttribute("uv", new THREE.Float32BufferAttribute(uv, 2)); g.setIndex(idx); return g;
}
/** TTF/OTF laden (vor dem ersten Seek!). Gibt THREE Font zurück. */
export async function loadFont(url) {
  const buf = await (await fetch(url)).arrayBuffer();
  return new Font(new TTFLoader().parse(buf));
}
/** 3D-Buchstaben. align: 'center' | 'left'. bevel in Welt-Einheiten. */
export function extrudeText(font, text, { size = 1, depth = 0.25, bevel = 0.02, bevelSegments = 4, curveSegments = 10, align = "center", letterSpacing = 0 } = {}) {
  let g;
  if (!letterSpacing) {
    g = new TextGeometry(text, { font, size, depth, curveSegments, bevelEnabled: bevel > 0, bevelThickness: bevel, bevelSize: bevel * 0.8, bevelSegments });
  } else { // Buchstabe für Buchstabe mit Sperrung
    const parts = []; let x = 0;
    for (const ch of text) {
      if (ch === " ") { x += size * 0.3 + letterSpacing; continue; }
      const p = new TextGeometry(ch, { font, size, depth, curveSegments, bevelEnabled: bevel > 0, bevelThickness: bevel, bevelSize: bevel * 0.8, bevelSegments });
      p.computeBoundingBox(); const w = p.boundingBox.max.x - p.boundingBox.min.x; p.translate(x - p.boundingBox.min.x, 0, 0); x += w + letterSpacing; parts.push(p);
    }
    g = BufferGeometryUtils.mergeGeometries(parts);
  }
  g.computeBoundingBox(); const bb = g.boundingBox;
  g.translate(align === "center" ? -(bb.max.x + bb.min.x) / 2 : -bb.min.x, -(bb.max.y + bb.min.y) / 2, -(bb.max.z + bb.min.z) / 2);
  return g;
}
/** Einzelne Buchstaben als eigene Geometrien (für Buchstaben-Animation), je zentriert + Offset. */
export function extrudeLetters(font, text, opts = {}) {
  const full = extrudeText(font, text, { ...opts, align: "left" }); full.computeBoundingBox();
  const W = full.boundingBox.max.x; const out = []; let x = 0; const size = opts.size || 1, ls = opts.letterSpacing || 0;
  for (const ch of text) {
    if (ch === " ") { x += size * 0.3 + ls; continue; }
    const g = extrudeText(font, ch, { ...opts, letterSpacing: 0, align: "left" }); g.computeBoundingBox();
    const w = g.boundingBox.max.x - g.boundingBox.min.x; g.translate(-w / 2, 0, 0);
    out.push({ char: ch, geometry: g, offset: new THREE.Vector3(x + w / 2 - W / 2, 0, 0) }); x += w + ls;
  }
  return out;
}
/** SVG-Pfade extrudieren (Logo). Gibt eine zusammengeführte, zentrierte Geometrie zurück; scale = Welt pro SVG-px. */
export function extrudeSVG(svgText, { depth = 0.2, scale = 0.01, bevel = 0.01, curveSegments = 24 } = {}) {
  const data = new SVGLoader().parse(svgText); const geos = [];
  for (const path of data.paths) for (const shape of SVGLoader.createShapes(path)) {
    geos.push(new THREE.ExtrudeGeometry(shape, { depth: depth / scale, bevelEnabled: bevel > 0, bevelThickness: bevel / scale, bevelSize: (bevel * 0.8) / scale, bevelSegments: 3, curveSegments }));
  }
  const g = BufferGeometryUtils.mergeGeometries(geos); g.scale(scale, -scale, scale); // SVG-y zeigt nach unten
  g.computeBoundingBox(); const c = g.boundingBox.getCenter(new THREE.Vector3()); g.translate(-c.x, -c.y, -c.z); g.computeVertexNormals();
  return g;
}

// ───────────────────────── Instancing: Schwarm mit Layouts ─────────────────────────
export const layouts = {
  grid(nx, ny, nz = 1, spacing = 0.2) {
    const out = [];
    for (let z = 0; z < nz; z++) for (let y = 0; y < ny; y++) for (let x = 0; x < nx; x++)
      out.push({ p: new THREE.Vector3((x - (nx - 1) / 2) * spacing, (y - (ny - 1) / 2) * spacing, (z - (nz - 1) / 2) * spacing) });
    return out;
  },
  sphere(n, r = 1, seed = 1) {
    const out = []; const ga = Math.PI * (3 - Math.sqrt(5)); const R = rng(seed);
    for (let i = 0; i < n; i++) { const y = 1 - (i / (n - 1)) * 2, rr = Math.sqrt(1 - y * y), a = i * ga;
      out.push({ p: new THREE.Vector3(Math.cos(a) * rr * r, y * r, Math.sin(a) * rr * r), r: new THREE.Euler(R() * 6.28, R() * 6.28, 0) }); }
    return out;
  },
  ring(n, r = 1, { y = 0, jitter = 0, seed = 1, faceOut = true } = {}) {
    const R = rng(seed); return Array.from({ length: n }, (_, i) => { const a = (i / n) * Math.PI * 2;
      return { p: new THREE.Vector3(Math.cos(a) * r + (R() - 0.5) * jitter, y + (R() - 0.5) * jitter, Math.sin(a) * r + (R() - 0.5) * jitter), r: faceOut ? new THREE.Euler(0, -a, 0) : undefined }; });
  },
  /** Punkte auf der Oberfläche einer Geometrie (z. B. extrudeText) — geseedet. */
  fromGeometry(geometry, n, seed = 1) {
    const s = new MeshSurfaceSampler(new THREE.Mesh(geometry)).setRandomGenerator(rng(seed)).build();
    const p = new THREE.Vector3(), nn = new THREE.Vector3(); const out = [];
    for (let i = 0; i < n; i++) { s.sample(p, nn); const q = new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0, 0, 1), nn); out.push({ p: p.clone(), q }); }
    return out;
  },
  scatter(n, box = [6, 4, 4], seed = 9) {
    const R = rng(seed); return Array.from({ length: n }, () => ({ p: new THREE.Vector3((R() - 0.5) * box[0], (R() - 0.5) * box[1], (R() - 0.5) * box[2]),
      r: new THREE.Euler(R() * 6.28, R() * 6.28, R() * 6.28), s: 0.6 + R() * 0.6 }));
  },
};
/**
 * Viele gleiche Teile als InstancedMesh, mit Übergängen zwischen Layouts (Morph, Explosion, Zusammenbau).
 * swarm.blend('a','b', u, {stagger, arc, spin, order}) setzt alle Instanzen für Fortschritt u (0..1).
 */
export class Swarm {
  constructor({ geometry, material, count, seed = 1 }) {
    this.count = count; this.R = rng(seed); this.mesh = new THREE.InstancedMesh(geometry, material, count);
    this.mesh.frustumCulled = false; this.mesh.castShadow = true; this.mesh.receiveShadow = true;
    this.layouts = {}; this.rand = Array.from({ length: count }, () => [this.R(), this.R(), this.R(), this.R(), this.R(), this.R()]);
    this._d = new THREE.Object3D();
  }
  layout(name, list) { // Liste wird auf count gestreckt/zyklisch aufgefüllt
    this.layouts[name] = Array.from({ length: this.count }, (_, i) => { const e = list[i % list.length];
      const q = e.q ? e.q.clone() : new THREE.Quaternion().setFromEuler(e.r || new THREE.Euler());
      return { p: e.p.clone(), q, s: e.s ?? 1 }; });
    return this;
  }
  /** order: 'random' | 'x' | 'y' | 'radial' | fn(i, from, to) -> 0..1 (wer zuerst startet) */
  blend(a, b, u, { stagger = 0.5, arc = 0.6, spin = 1, order = "random", easing = ease.inOut, scaleMid = 1 } = {}) {
    const A = this.layouts[a], B = this.layouts[b]; const d = this._d;
    let ord = null;
    if (order !== "random") {
      const key = (i) => (typeof order === "function" ? order(i, A[i], B[i]) : order === "x" ? A[i].p.x : order === "y" ? A[i].p.y : A[i].p.length());
      const vals = Array.from({ length: this.count }, (_, i) => key(i)); const mn = Math.min(...vals), mx = Math.max(...vals);
      ord = vals.map((v) => (mx > mn ? (v - mn) / (mx - mn) : 0));
    }
    const ax = new THREE.Vector3(), qs = new THREE.Quaternion();
    for (let i = 0; i < this.count; i++) {
      const r = this.rand[i]; const start = (ord ? ord[i] : r[0]) * stagger;
      const k = easing(clamp01((u - start) / Math.max(1e-4, 1 - stagger)));
      const p0 = A[i].p, p1 = B[i].p; const mid = p0.clone().add(p1).multiplyScalar(0.5);
      const out = mid.clone().normalize().multiplyScalar(arc * (0.5 + r[1])).add(new THREE.Vector3((r[2] - 0.5) * arc, (r[3] - 0.2) * arc, (r[4] - 0.5) * arc));
      const ctrl = mid.add(out); const m = 1 - k;
      d.position.set(0, 0, 0).addScaledVector(p0, m * m).addScaledVector(ctrl, 2 * m * k).addScaledVector(p1, k * k);
      d.quaternion.slerpQuaternions(A[i].q, B[i].q, k);
      if (spin) { ax.set(r[3] - 0.5, r[4] - 0.5, r[5] - 0.5).normalize(); qs.setFromAxisAngle(ax, Math.sin(Math.PI * k) * spin * Math.PI); d.quaternion.premultiply(qs); }
      const s = lerp(A[i].s, B[i].s, k) * lerp(1, scaleMid, Math.sin(Math.PI * k)); d.scale.setScalar(s);
      d.updateMatrix(); this.mesh.setMatrixAt(i, d.matrix);
    }
    this.mesh.instanceMatrix.needsUpdate = true;
    return this;
  }
  set(name) { return this.blend(name, name, 1); }
}

// ───────────────────────── Kamera-Rig mit Shot-Liste ─────────────────────────
/**
 * shots: [{ start, end, pos, target, lens, focus, bokeh, ease, roll, shake, name }]
 *  pos/target: [x,y,z] (steht) | [[…],[…]] (Fahrt linear) | ≥3 Punkte (Catmull-Rom-Fahrt) | fn(u,t) -> Vector3
 *  lens: Brennweite mm (Vollformat) oder [von, bis]. Makro: 85–135 mm nah dran + kleiner focus.
 *  focus: Zahl (Abstand) | Object3D | [x,y,z] | 'target' (Standard) — setzt die Schärfeebene.
 *  bokeh: Unschärfe in px für Unendlich (überschreibt post.dof.bokeh), auch [von, bis] (Schärfe ziehen über focus-Liste).
 * Zwischen zwei Shots = harter Schnitt. Durchgehende Fahrt = ein Shot mit mehreren Pfadpunkten.
 */
export function shotRig(shots) {
  const cuts = shots.map((s) => s.start);
  const resolve = (spec, u, t) => {
    if (typeof spec === "function") return spec(u, t);
    if (spec instanceof THREE.Object3D) return spec.getWorldPosition(new THREE.Vector3());
    if (!Array.isArray(spec[0])) return v3(spec);
    if (spec.length === 2) return v3(spec[0]).lerp(v3(spec[1]), u);
    return new THREE.CatmullRomCurve3(spec.map(v3), false, "centripetal").getPoint(u);
  };
  const num = (x, u) => (Array.isArray(x) ? (x.length === 2 ? lerp(x[0], x[1], u) : (() => { const f = u * (x.length - 1), i = Math.min(x.length - 2, Math.floor(f)); return lerp(x[i], x[i + 1], f - i); })()) : x);
  function at(t) {
    let i = shots.length - 1; for (let k = 0; k < shots.length; k++) if (t < shots[k].end) { i = k; break; }
    const s = shots[i]; const raw = clamp01((t - s.start) / (s.end - s.start)); const fn = typeof s.ease === "function" ? s.ease : ease[s.ease || "inOut"];
    return { shot: s, index: i, u: fn(raw), raw, local: t - s.start };
  }
  function apply(t, camera, post) {
    const { shot: s, u, raw } = at(t);
    const pos = resolve(s.pos, u, t), tgt = resolve(s.target ?? [0, 0, 0], u, t);
    if (s.shake) { const k = s.shake, f = s.shakeFreq || 1.3; pos.x += noise1(t * f, 1) * k; pos.y += noise1(t * f, 2) * k * 0.7; tgt.x += noise1(t * f, 3) * k * 0.5; tgt.y += noise1(t * f, 4) * k * 0.5; }
    camera.position.copy(pos); camera.up.set(0, 1, 0); camera.lookAt(tgt);
    if (s.roll) camera.rotateZ(THREE.MathUtils.degToRad(num(s.roll, u)));
    camera.setFocalLength(num(s.lens ?? 50, u)); camera.updateProjectionMatrix();
    if (post && post.dof) {
      const f = s.focus ?? "target"; let dist;
      if (typeof f === "number") dist = f; else if (Array.isArray(f) && typeof f[0] === "number" && f.length === 3) dist = pos.distanceTo(v3(f));
      else if (Array.isArray(f)) { dist = num(f.map((x) => (typeof x === "number" ? x : pos.distanceTo(resolve(x, u, t)))), s.focusEase ? ease[s.focusEase](raw) : u); }
      else if (f instanceof THREE.Object3D) dist = pos.distanceTo(f.getWorldPosition(new THREE.Vector3()));
      else dist = pos.distanceTo(tgt);
      post.setFocus(dist, s.bokeh != null ? num(s.bokeh, u) : null);
    }
    return at(t);
  }
  return { shots, cuts, at, apply };
}

// ───────────────────────── Postprocessing ─────────────────────────
const FS_VERT = `varying vec2 vUv; void main(){ vUv = uv; gl_Position = vec4(position.xy, 0.0, 1.0); }`;
// Tiefenunschärfe: Ein-Pass-Bokeh mit Goldener-Winkel-Spirale (nach D. Gustafsson), HDR-Glanzlichter werden Scheiben.
const DOF_FRAG = `
#include <packing>
varying vec2 vUv; uniform sampler2D tColor; uniform sampler2D tDepth; uniform vec2 uPixel;
uniform float uFocus, uBokeh, uMaxBlur, uRadScale, uNear, uFar;
float viewZ(vec2 uv){ return -perspectiveDepthToViewZ(texture2D(tDepth, uv).x, uNear, uFar); }
float coc(float d){ return clamp(uBokeh * abs(1.0 - uFocus / max(d, 1e-4)), 0.0, uMaxBlur); }
void main(){
  float cD = viewZ(vUv); float cS = coc(cD);
  vec3 c = texture2D(tColor, vUv).rgb; float tot = 1.0; float radius = uRadScale;
  for (int i = 0; i < 1200; i++) {
    if (radius >= uMaxBlur) break;
    float ang = float(i) * 2.39996323;
    vec2 tc = vUv + vec2(cos(ang), sin(ang)) * uPixel * radius;
    vec3 sc = texture2D(tColor, tc).rgb; float sD = viewZ(tc); float sS = coc(sD);
    if (sD > cD) sS = clamp(sS, 0.0, cS * 2.0);
    float m = smoothstep(radius - 0.5, radius + 0.5, sS);
    c += mix(c / tot, sc, m); tot += 1.0; radius += uRadScale / radius;
  }
  gl_FragColor = vec4(c / tot, 1.0);
}`;
// Ausgabe: Belichtung, ACES/Neutral, sRGB, Vignette, chromatische Aberration, Filmkorn (aus t geseedet), Dither.
const OUT_FRAG = `
varying vec2 vUv; uniform sampler2D tColor; uniform float uExposure, uVignette, uGrain, uAberr, uTime; uniform vec2 uRes; uniform int uTone;
vec3 RRTAndODTFit(vec3 v){ vec3 a = v*(v+0.0245786)-0.000090537; vec3 b = v*(0.983729*v+0.4329510)+0.238081; return a/b; }
vec3 aces(vec3 color){
  const mat3 I = mat3(vec3(0.59719,0.07600,0.02840), vec3(0.35458,0.90834,0.13383), vec3(0.04823,0.01566,0.83777));
  const mat3 O = mat3(vec3(1.60475,-0.10208,-0.00327), vec3(-0.53108,1.10813,-0.07276), vec3(-0.07367,-0.00605,1.07602));
  color *= 1.0/0.6; color = I*color; color = RRTAndODTFit(color); color = O*color; return clamp(color,0.0,1.0); }
vec3 neutral(vec3 color){ const float S = 0.76; const float D = 0.15; float x = min(color.r, min(color.g, color.b));
  float off = x < 0.08 ? x - 6.25*x*x : 0.04; color -= off; float peak = max(color.r, max(color.g, color.b)); if (peak < S) return color;
  float d = 1.0 - S; float np = 1.0 - d*d/(peak + d - S); color *= np/peak; float g = 1.0 - 1.0/(D*(peak-np)+1.0); return mix(color, vec3(np), g); }
vec3 toSRGB(vec3 c){ c = max(c, 0.0); return mix(1.055*pow(c, vec3(1.0/2.4)) - 0.055, c*12.92, vec3(lessThanEqual(c, vec3(0.0031308)))); }
float hash(vec3 p){ p = fract(p*0.3183099 + 0.1); p *= 17.0; return fract(p.x*p.y*p.z*(p.x+p.y+p.z)); }
void main(){
  vec2 d = vUv - 0.5; vec3 c;
  if (uAberr > 0.0) { vec2 o = d * uAberr / uRes.x * 2.0; c = vec3(texture2D(tColor, vUv + o).r, texture2D(tColor, vUv).g, texture2D(tColor, vUv - o).b); }
  else c = texture2D(tColor, vUv).rgb;
  c *= uExposure;
  c = uTone == 1 ? neutral(c) : (uTone == 2 ? clamp(c,0.0,1.0) : aces(c));
  float v = 1.0 - uVignette * smoothstep(0.25, 0.95, length(d * vec2(uRes.x/uRes.y, 1.0)) / 0.9);
  c = toSRGB(c * v);
  float n = hash(vec3(gl_FragCoord.xy, floor(uTime * 60.0) + 1.0)) - 0.5;
  float lum = dot(c, vec3(0.299,0.587,0.114)); c += n * uGrain * (1.0 - lum * 0.6) + (hash(vec3(gl_FragCoord.yx, 7.0)) - 0.5) / 255.0;
  gl_FragColor = vec4(c, 1.0);
}`;

class Post {
  constructor(renderer, w, h, o) {
    this.renderer = renderer; this.w = w; this.h = h;
    this.o = { dof: o.dof === false ? false : { bokeh: 10, maxBlur: 22, quality: 0.8, ...(o.dof || {}) },
      bloom: o.bloom === false ? false : { strength: 0.35, radius: 0.55, threshold: 1.0, ...(o.bloom || {}) },
      grain: o.grain ?? 0.035, vignette: o.vignette ?? 0.22, aberration: o.aberration ?? 0.6, tone: o.tone || "aces", exposure: o.exposure ?? 1,
      msaa: o.msaa ?? 4 };
    const opt = { type: THREE.HalfFloatType, colorSpace: THREE.LinearSRGBColorSpace, depthBuffer: true };
    this.rtScene = new THREE.WebGLRenderTarget(w, h, { ...opt, samples: this.o.msaa });
    this.rtScene.depthTexture = new THREE.DepthTexture(w, h, THREE.FloatType);
    this.rtA = new THREE.WebGLRenderTarget(w, h, { ...opt, depthBuffer: false });
    this.rtAcc = new THREE.WebGLRenderTarget(w, h, { ...opt, depthBuffer: false });
    this.dofQ = new FullScreenQuad(new THREE.ShaderMaterial({ vertexShader: FS_VERT, fragmentShader: DOF_FRAG, toneMapped: false, depthTest: false, depthWrite: false,
      uniforms: { tColor: { value: null }, tDepth: { value: null }, uPixel: { value: new THREE.Vector2(1 / w, 1 / h) }, uFocus: { value: 5 },
        uBokeh: { value: 10 }, uMaxBlur: { value: 22 }, uRadScale: { value: 0.8 }, uNear: { value: 0.1 }, uFar: { value: 100 } } }));
    // Additiv: rgb·uW wird aufsummiert (Mittelwert der Zwischenbilder). Normal-Blending würde abdunkeln.
    this.accQ = new FullScreenQuad(new THREE.ShaderMaterial({ vertexShader: FS_VERT, toneMapped: false, depthTest: false, depthWrite: false, transparent: true,
      blending: THREE.AdditiveBlending, premultipliedAlpha: false,
      uniforms: { tColor: { value: null }, uW: { value: 1 } }, fragmentShader: `varying vec2 vUv; uniform sampler2D tColor; uniform float uW; void main(){ gl_FragColor = vec4(texture2D(tColor, vUv).rgb, uW); }` }));
    this.outQ = new FullScreenQuad(new THREE.ShaderMaterial({ vertexShader: FS_VERT, fragmentShader: OUT_FRAG, toneMapped: false, depthTest: false, depthWrite: false,
      uniforms: { tColor: { value: null }, uExposure: { value: 1 }, uVignette: { value: 0 }, uGrain: { value: 0 }, uAberr: { value: 0 }, uTime: { value: 0 },
        uRes: { value: new THREE.Vector2(w, h) }, uTone: { value: 0 } } }));
    if (this.o.bloom) this.bloom = new UnrealBloomPass(new THREE.Vector2(w, h), this.o.bloom.strength, this.o.bloom.radius, this.o.bloom.threshold);
    this.focus = 5; this.bokehOverride = null;
  }
  get dof() { return this.o.dof; }
  setFocus(dist, bokeh = null) { this.focus = dist; this.bokehOverride = bokeh; }
  /** Szene (+DoF) in Ziel rendern. */
  _scene(scene, camera, target) {
    const r = this.renderer;
    if (!this.o.dof) { r.setRenderTarget(target === "scene" ? this.rtScene : target); r.clear(); r.render(scene, camera); return; }
    r.setRenderTarget(this.rtScene); r.clear(); r.render(scene, camera);
    const u = this.dofQ.material.uniforms;
    u.tColor.value = this.rtScene.texture; u.tDepth.value = this.rtScene.depthTexture; u.uFocus.value = this.focus;
    u.uBokeh.value = this.bokehOverride ?? this.o.dof.bokeh; u.uMaxBlur.value = this.o.dof.maxBlur; u.uRadScale.value = 1.0 / Math.max(0.2, this.o.dof.quality);
    u.uNear.value = camera.near; u.uFar.value = camera.far;
    r.setRenderTarget(target === "scene" ? this.rtA : target); this.dofQ.render(r);
  }
  /** render(t, updateFn, scene, camera, motionBlur) */
  render(t, update, scene, camera, mb) {
    const r = this.renderer; let src;
    if (mb && mb.samples > 1) {
      r.setRenderTarget(this.rtAcc); r.setClearColor(0x000000, 0); r.clear();
      for (let k = 0; k < mb.samples; k++) {
        let tt = t + ((k + 0.5) / mb.samples - 0.5) * (mb.shutter ?? 0.5) / (mb.fps || 30);
        if (mb.lo != null) tt = Math.min(Math.max(tt, mb.lo), mb.hi - 1e-4); // nie über einen Schnitt hinweg mitteln
        update(tt); this._scene(scene, camera, "scene");
        const a = this.accQ.material.uniforms; a.tColor.value = this.o.dof ? this.rtA.texture : this.rtScene.texture; a.uW.value = 1 / mb.samples;
        r.setRenderTarget(this.rtAcc); const ac = r.autoClear; r.autoClear = false; this.accQ.render(r); r.autoClear = ac; // sonst löscht jedes Zwischenbild das vorige
      }
      update(t); src = this.rtAcc;
    } else {
      update(t); this._scene(scene, camera, "scene"); src = this.o.dof ? this.rtA : this.rtScene;
    }
    if (this.bloom) this.bloom.render(r, null, src, 0, false);
    const u = this.outQ.material.uniforms;
    u.tColor.value = src.texture; u.uExposure.value = this.o.exposure; u.uVignette.value = this.o.vignette; u.uGrain.value = this.o.grain;
    u.uAberr.value = this.o.aberration; u.uTime.value = t; u.uTone.value = this.o.tone === "neutral" ? 1 : this.o.tone === "none" ? 2 : 0;
    r.setRenderTarget(null); this.outQ.render(r);
  }
}

// ───────────────────────── Studio: alles zusammen ─────────────────────────
/**
 * const studio = createStudio({ canvas, env:'studio', background:{…}, post:{dof:{…}, bloom:{…}} })
 * studio.run((t) => { rig.apply(t, studio.camera, studio.post); …Objekte aus t setzen… })
 */
export function createStudio({ canvas, width = 1920, height = 1080, fps = 30, env = "studio", envOptions = {}, envIntensity = 1, envRotation = 0,
  background = {}, shadows = true, post = {}, exposure = 1, tone = "aces", motionBlur = null, pixelRatio = 1 } = {}) {
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: post === false, alpha: false, preserveDrawingBuffer: true, powerPreference: "high-performance" });
  renderer.setPixelRatio(pixelRatio); renderer.setSize(width, height, false);
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = post === false ? (tone === "neutral" ? THREE.NeutralToneMapping : THREE.ACESFilmicToneMapping) : THREE.NoToneMapping;
  renderer.toneMappingExposure = exposure;
  renderer.shadowMap.enabled = !!shadows; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.setClearColor(0x000000, 1);
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(30, width / height, 0.05, 200);
  if (env) {
    const pm = new THREE.PMREMGenerator(renderer);
    const envScene = env === "room" ? new RoomEnvironment() : env === "studio" ? studioEnvScene(envOptions) : env;
    scene.environment = pm.fromScene(envScene, 0.035).texture; pm.dispose();
  }
  scene.environmentIntensity = envIntensity; scene.environmentRotation.set(0, envRotation, 0);
  let bg = null; if (background) { bg = gradientBackground(background); scene.add(bg); }
  const P = post === false ? null : new Post(renderer, width, height, { ...post, tone, exposure });
  const studio = {
    THREE, renderer, scene, camera, background: bg, post: P, fps, width, height, motionBlur, cuts: [],
    add(...o) { scene.add(...o); return o[0]; },
    /** Ein Bild zu Zeit t. update(t) setzt Kamera + Objekte (reine Funktion von t). */
    renderAt(t, update) {
      const mbv = typeof motionBlur === "function" ? motionBlur(t) : motionBlur;
      let lo = null, hi = null; // Einstellungsgrenzen aus studio.cuts (rig.cuts), damit Zwischenbilder nicht ins Nachbarbild greifen
      if (mbv && studio.cuts.length) { lo = 0; hi = Infinity; for (const c of studio.cuts) { if (c <= t) lo = Math.max(lo, c); else hi = Math.min(hi, c); } }
      if (P) P.render(t, update, scene, camera, mbv && { fps, lo, hi, ...mbv });
      else { update(t); renderer.setRenderTarget(null); renderer.render(scene, camera); }
    },
    /** Verdrahtet HyperFrames-Seek. ready: optionales Promise (Fonts, Geometrie), wird als buildReady angemeldet. */
    run(update, { ready = null, key = "hf3d", cuts = null } = {}) {
      if (cuts) studio.cuts = cuts;
      const go = (t) => studio.renderAt(t, update);
      const start = (ready || Promise.resolve()).then(() => {
        renderer.compile(scene, camera); go(window.__hfThreeTime || 0);
        window.addEventListener("hf-seek", (e) => go(e.detail.time));
      });
      window.__hf = window.__hf || {}; window.__hf.buildReady = window.__hf.buildReady || {};
      window.__hf.buildReady[key] = start; return start;
    },
  };
  return studio;
}

/** Schatten für alle Meshes eines Objekts einschalten. */
export function castAll(obj, cast = true, receive = true) { obj.traverse((m) => { if (m.isMesh) { m.castShadow = cast; m.receiveShadow = receive; } }); return obj; }
