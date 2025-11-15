require('events').setMaxListeners(20);

module.exports = {
  devServer: {
    proxy: {
      '/auth': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
      },
      '/users': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
      },
      '/rentals': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
      },
      '/financial_summary': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
      },
      '/objects': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
      },
      '/status_history': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
      },
    },
    port: 8081,
    host: '127.0.0.1',
  },
};

