import {
  AbsoluteFill,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
  Img,
} from "remotion";
import React, { useEffect, useRef, useState } from "react";
import * as maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import { AnimatedBorder } from "./components/AnimatedBorder";
import { YellowLabel } from "./components/YellowLabel";
import { Caption } from "./components/Caption";

function interpolateCamera(frame: number, keyframes: any[]) {
  if (!keyframes || keyframes.length === 0) return null;
  if (keyframes.length === 1) {
    const target = keyframes[0];
    return {
      lng: target.center[0],
      lat: target.center[1],
      zoom: target.zoom,
      pitch: target.pitch,
      bearing: target.bearing,
    };
  }

  let startKf = keyframes[0];
  let endKf = keyframes[keyframes.length - 1];

  for (let i = 0; i < keyframes.length - 1; i++) {
    if (frame >= keyframes[i].frame && frame <= keyframes[i + 1].frame) {
      startKf = keyframes[i];
      endKf = keyframes[i + 1];
      break;
    }
  }

  if (frame <= keyframes[0].frame) {
    const target = keyframes[0];
    return {
      lng: target.center[0],
      lat: target.center[1],
      zoom: target.zoom,
      pitch: target.pitch,
      bearing: target.bearing,
    };
  }
  if (frame >= keyframes[keyframes.length - 1].frame) {
    const target = keyframes[keyframes.length - 1];
    return {
      lng: target.center[0],
      lat: target.center[1],
      zoom: target.zoom,
      pitch: target.pitch,
      bearing: target.bearing,
    };
  }

  const range = [startKf.frame, endKf.frame];

  return {
    lng: interpolate(frame, range, [startKf.center[0], endKf.center[0]]),
    lat: interpolate(frame, range, [startKf.center[1], endKf.center[1]]),
    zoom: interpolate(frame, range, [startKf.zoom, endKf.zoom]),
    pitch: interpolate(frame, range, [startKf.pitch, endKf.pitch]),
    bearing: interpolate(frame, range, [startKf.bearing, endKf.bearing]),
  };
}

export const GenericComposition: React.FC<any> = ({
  cameraKeyframes = [],
  mapHighlights = [],
  textOverlays = [],
  blackScreens = [],
  iconOverlays = [],
  imageOverlays = [],
  movingIcons = [],
}) => {
  console.log("PROPS DEBUG:", { cameraKeyframes, mapHighlights });
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();
  const mapContainer = useRef<HTMLDivElement>(null);
  const [mapInstance, setMapInstance] = useState<maplibregl.Map | null>(null);
  const [borderData, setBorderData] = useState<any>(null);

    // ?? CONVENTION OVER CONFIGURATION:
  // Instead of hardcoding which map files to load, we dynamically read your `Root.tsx` config.
  // If you typed `layer: "china-fill"`, we slice off the "-fill" to extract the word "china".
  // This automatically builds a list of exactly which countries you need for this specific video!
  const uniqueRegions = Array.from(new Set(mapHighlights.map((h: any) => h.layer.split('-')[0])));

  // 1. ?? AUTO-FETCH & AUTO-FORMAT ENGINE (The "Mailroom Clerk")
  // Why: MapLibre is extremely strict. It refuses to load data unless it is perfectly formatted as a `FeatureCollection`.
  // What this does: It takes your `uniqueRegions` list, automatically finds the `.json` files in `public/data/`,
  // downloads them, checks if they are dirty Nominatim search arrays, and instantly cleans them if needed!
  useEffect(() => {
    const fetchPromises = uniqueRegions.map(region => 
      fetch(staticFile(`data/${region}.json`))
        .then(r => r.json())
        .then(data => {
            // Auto-format raw Nominatim API arrays into valid FeatureCollections!
            if (Array.isArray(data) && data.length > 0 && data[0].geojson) {
               return { region, data: {
                 type: "FeatureCollection",
                 features: [{ type: "Feature", properties: { name: data[0].display_name }, geometry: data[0].geojson }]
               }};
            }
            return { region, data };
        })
        .catch(e => null) // Silently ignore if file doesn't exist
    );

    Promise.all(fetchPromises).then(results => {
      const borders: any = {};
      results.forEach(res => {
        if (res) {
            borders[`${res.region}-fill`] = res.data;
            borders[`${res.region}-border`] = res.data;
            borders[`${res.region}-line`] = res.data;
        }
      });
      setBorderData(borders);
    });
  }, [uniqueRegions.join(',')]); // Refresh if a completely new region is added to Root.tsx

  // 2. Initialize the MapLibre Map Canvas
  useEffect(() => {
    if (!mapContainer.current) return;

    const map = new maplibregl.Map({
      container: mapContainer.current,
      style: {
        version: 8,
        sources: {
          "esri-raster": {
            type: "raster",
            tiles: [
              "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
            ],
            tileSize: 256,
          },
        },
        layers: [], // REMOVED ESRI LAYER
      },
      center: [0, 0],
      zoom: 2,
      interactive: false,
      fadeDuration: 0,
      attributionControl: false,
      canvasContextAttributes: { preserveDrawingBuffer: true },
    });

        map.on("load", () => {
      setMapInstance(map);
      
      // ?? COORDINATE CLICKER (Dev Tool)
      // Why: Finding exact longitude/latitude for popping up images (like corn.png) is annoying.
      // What this does: Open Chrome DevTools (F12). Click anywhere on the map in the video preview. 
      // It instantly prints the exact coordinates to the console so you can copy/paste them into Root.tsx!
      map.on("click", (e) => {
        console.log(`[${e.lngLat.lng.toFixed(4)}, ${e.lngLat.lat.toFixed(4)}]`);
      });
    });

    // Let the browser dispose of the map instance
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // 2.5 ?? AUTO-REGISTER MAP LAYERS
  // Why: Usually, you have to write 20 lines of Mapbox code to register a source and a layer for every single country.
  // What this does: Because we already downloaded the clean map data in Step 1, this loop tells MapLibre:
  // "Hey, create a hidden layer called 'china-fill' and 'china-border' and hook them up." 
  // It sets the opacity to 0 so they stay perfectly invisible until Root.tsx tells them to appear!
  useEffect(() => {
      if (!mapInstance || !borderData) return;
      
      uniqueRegions.forEach(region => {
          const geojsonData = borderData[`${region}-fill`];
          if (!geojsonData) return;
          
          if (!mapInstance.getSource(`${region}-source`)) {
              mapInstance.addSource(`${region}-source`, {
                  type: "geojson",
                  data: geojsonData // Pass the auto-formatted object!
              });
          }
          
          if (!mapInstance.getLayer(`${region}-fill`)) {
              mapInstance.addLayer({
                  id: `${region}-fill`,
                  type: "fill",
                  source: `${region}-source`,
                  paint: { "fill-color": "#ff0000", "fill-opacity": 1 }
              });
          }
          if (!mapInstance.getLayer(`${region}-border`)) {
              mapInstance.addLayer({
                  id: `${region}-border`,
                  type: "line",
                  source: `${region}-source`,
                  paint: { "line-color": "#ffffff", "line-opacity": 0, "line-width": 2 }
              });
          }
          if (!mapInstance.getLayer(`${region}-line`)) {
              mapInstance.addLayer({
                  id: `${region}-line`,
                  type: "line",
                  source: `${region}-source`,
                  paint: { "line-color": "#ffffff", "line-opacity": 0, "line-width": 2 }
              });
          }
      });
  }, [mapInstance, borderData]);

  // 3. Dynamic Frame Updates (Camera & Styling)
  useEffect(() => {
    if (!mapInstance) return;

    // 1. Camera interpolation
    const cam = interpolateCamera(frame, cameraKeyframes);
    if (cam) {
      mapInstance.jumpTo({
        center: [cam.lng, cam.lat],
        zoom: cam.zoom,
        pitch: cam.pitch,
        bearing: cam.bearing,
      });
    }

    // ?? DATA-DRIVEN STYLING ENGINE (The "Puppeteer")
    // Why: We don't want to use standard CSS animations because Remotion renders frames out-of-order, causing flickering.
    // What this does: It constantly listens to `useCurrentFrame()`. If the current frame is between
    // your `startFrame` and `endFrame` in Root.tsx, it instantly flips the map opacity from 0 to 0.8 and paints the color!
    const uniqueLayers = Array.from(new Set(mapHighlights.map((h: any) => h.layer)));
    uniqueLayers.forEach((layerId) => {
      const lid = layerId as string;
      if (mapInstance.getLayer(lid)) {
        const activeHl = mapHighlights.find(
          (h: any) =>
            h.layer === lid && frame >= h.startFrame && frame <= h.endFrame,
        );
        const opacityProp = lid.includes("fill") ? "fill-opacity" : "line-opacity";
        const colorProp = lid.includes("fill") ? "fill-color" : "line-color";

        // Deterministic Zero-Hardcoding defaults
        const defaultOpacity = 0;
        const defaultColor = "transparent";

        // mapInstance.setPaintProperty(
        //   lid,
        //   opacityProp,
        //   activeHl ? activeHl.opacity : defaultOpacity,
        // );

        const targetColor = (activeHl && activeHl.color) ? activeHl.color : defaultColor;

        // Handle special keyword "preserve" to extract colors directly from GeoJSON properties
        const parsedColor = targetColor === "preserve" ? ["get", "color"] : targetColor;

        if (parsedColor) {
          try {
            // mapInstance.setPaintProperty(lid, colorProp, parsedColor);
          } catch (e) {
            // Ignore
          }
        }

        if (activeHl && activeHl.width !== undefined && lid.includes("line")) {
          mapInstance.setPaintProperty(lid, "line-width", activeHl.width);
        }
      }
    });
  }, [frame, mapInstance, cameraKeyframes, mapHighlights, borderData]);

  const isBlackScreen = blackScreens.some(
    (bs: any) => frame >= bs.startFrame && frame <= bs.endFrame,
  );

  return (
    <AbsoluteFill style={{ backgroundColor: isBlackScreen ? "black" : "transparent" }}>
      {/* 1. BACKGROUND ENGINE */}
      <div
        ref={mapContainer}
        style={{
          position: "absolute",
          width: `${width}px`,
          height: `${height}px`,
          opacity: isBlackScreen ? 0 : 1,
        }}
      />
      
      {/* 2. SVG ANIMATED BORDERS */}
      {mapInstance && borderData &&
        mapHighlights.map((hl: any, i: number) => {
          if (hl.svgDraw && borderData[hl.layer]) {
            return (
              <AnimatedBorder
                key={`border-${i}`}
                map={mapInstance}
                frame={frame}
                geojson={borderData[hl.layer]}
                startFrame={hl.startFrame}
                endFrame={hl.endFrame}
                color={hl.color}
                width={hl.width}
                drawKeyframes={hl.drawKeyframes}
                mainlandOnly={hl.layer === "india-border"}
              />
            );
          }
          return null;
        })}

      {/* 3. OVERLAYS (TEXT & ICONS) */}
      {textOverlays.map((t: any, i: number) => {
        if (frame >= t.startFrame && frame <= t.endFrame) {
          // ?? COMPONENT DISCRIMINATOR (Stop Using Inline CSS!)
          // Why: Writing font sizes and shadows inside `Root.tsx` makes the file bloated.
          // What this does: If it sees `type: "yellow-label"`, it delegates all rendering to your dedicated React Component.
          // It passes along your text, and any optional overrides (like position or rotation).
          if (t.type === "yellow-label") {
             return <YellowLabel key={i} text={t.text} top={t.top} left={t.left} fontSize={t.fontSize} rotation={t.rotation} />;
          }
          return (
            <div key={i} style={{ position: "absolute", ...t.style }}>
              {t.text}
            </div>
          );
        }
        return null;
      })}

      {[...iconOverlays, ...imageOverlays].map((icon: any, i: number) => {
        if (frame >= icon.startFrame && frame <= icon.endFrame) {
          const s = spring({
            fps,
            frame: frame - icon.startFrame,
            config: { damping: 14, mass: 0.8 },
          });

          // Geospatial Projection Mode (stick to map surface)
          if (icon.coords && mapInstance) {
             return icon.coords.map((coord: [number, number], j: number) => {
               const pos = mapInstance.project(coord);
               return (
                  <Img
                    key={`icon-${i}-${j}`}
                    src={staticFile(icon.src)}
                    style={{
                      position: 'absolute',
                      left: pos.x,
                      top: pos.y,
                      width: icon.width || '50px',
                      height: icon.height || '50px',
                      transform: `translate(-50%, -50%) ${icon.rotation || ""} scale(${s})`,
                      filter: 'drop-shadow(5px 5px 10px rgba(0,0,0,0.7))',
                      pointerEvents: 'none'
                    }}
                  />
               )
             })
          }

          // Standard CSS Mode
          return (
            <Img
              key={`icon-${i}`}
              src={staticFile(icon.src)}
              style={{
                position: icon.position || "absolute",
                top: icon.top,
                left: icon.left,
                width: icon.width,
                height: icon.height,
                objectFit: icon.objectFit as any,
                border: icon.border,
                boxShadow: icon.boxShadow,
                borderRadius: icon.borderRadius,
                transform: `translate(-50%, -50%) ${icon.rotation || ""} scale(${s})`,
              }}
            />
          );
        }
        return null;
      })}

      {/* 4. MOVING ICONS */}
      {movingIcons && movingIcons.map((icon: any, i: number) => {
        if (frame >= icon.startFrame && frame <= icon.endFrame && mapInstance) {
          const progress = (frame - icon.startFrame) / (icon.endFrame - icon.startFrame);
          const currentLon = interpolate(progress, [0, 1], [icon.startCoords[0], icon.endCoords[0]]);
          const currentLat = interpolate(progress, [0, 1], [icon.startCoords[1], icon.endCoords[1]]);
          
          const pos = mapInstance.project([currentLon, currentLat]);
          
          return (
            <Img
              key={`moving-${i}`}
              src={staticFile(icon.src)}
              style={{
                position: 'absolute',
                left: pos.x,
                top: pos.y,
                width: icon.width || '50px',
                height: icon.height || '50px',
                transform: `translate(-50%, -50%)`,
                filter: 'drop-shadow(5px 5px 10px rgba(0,0,0,0.7))',
                pointerEvents: 'none'
              }}
            />
          );
        }
        return null;
      })}

      {/* DEBUG OUTPUT SO I CAN SEE WHAT'S HAPPENING */}
      <h1 style={{ position: 'absolute', zIndex: 9999, color: 'red', fontSize: '100px', top: '100px' }}>
        DEBUG: Borders loaded: {Object.keys(borderData || {}).length}
        <br />
        {mapHighlights.map((h:any) => `HL: ${h.layer} (${h.startFrame}-${h.endFrame})`).join(", ")}
      </h1>

      {/* 5. CAPTIONS */}
      <Caption frame={frame} />
    </AbsoluteFill>
  );
};
