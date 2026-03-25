/** @type {import('next').NextConfig} */
const nextConfig = {
  productionBrowserSourceMaps: false,
  swcMinify: true,
  compress: true,
  poweredByHeader: false,
};

module.exports = nextConfig;
