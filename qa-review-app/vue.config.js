// vue.config.js
module.exports = {
  devServer: {
    proxy: {
      "/api": {
        target: "http://localhost:8000", // Your backend server URL
        ws: true,
        changeOrigin: true,
      },
    },
  },
  chainWebpack: (config) => {
    config.plugin("define").tap((definitions) => {
      Object.assign(definitions[0], {
        __VUE_OPTIONS_API__: true,
        __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: false,
      });
      return definitions;
    });
  },
};
