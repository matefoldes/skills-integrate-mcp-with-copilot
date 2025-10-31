import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  async rewrites() {
    return [
      {
        source: '/activities/:path*',
        destination: 'http://localhost:8000/activities/:path*',
      },
    ];
  },
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'octodex.github.com',
        pathname: '/images/**',
      },
    ],
  },
};

export default nextConfig;
