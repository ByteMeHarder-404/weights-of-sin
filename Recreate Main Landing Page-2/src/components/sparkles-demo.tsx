"use client";
import React from "react";
import { SparklesCore } from "./ui/sparkles";

export default function SparklesPreview() {
  return (
    <div className="h-[20rem] w-full flex flex-col items-center justify-center overflow-hidden rounded-md bg-black/90">
      <div className="w-full h-full relative">
        {/* Core component */}
        <SparklesCore
          background="black"
          minSize={0.6}
          maxSize={2}
          particleDensity={3000}
          className="w-full h-full"
          particleColor="#9fb88c"
          speed={2}
        />
      </div>
    </div>
  );
}