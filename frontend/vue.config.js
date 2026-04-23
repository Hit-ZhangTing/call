module.exports = {
  devServer: {
    https: false,
    host: 'localhost',
    port: 8080,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        secure: false
      }
    }
  }
}
