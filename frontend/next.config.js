/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Configuração para Netlify
  output: 'standalone',
  images: {
    unoptimized: true,
  },
}

module.exports = nextConfig
