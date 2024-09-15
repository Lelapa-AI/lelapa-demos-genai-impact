const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");

module.exports = {
  mode: "production", // Adjust to "production" for optimized builds
  entry: "./App.js",
  output: {
    filename: "bundle.js",
    path: path.resolve(__dirname, "dist"),
  },
  module: {
    rules: [
      {
        test: /\.(m?js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
          options: {
            presets: [
              [
                "@babel/preset-env",

                { modules: false },
                // {
                //   targets: {
                //     // Specify your target browsers or environments here
                //     browsers: ["> 1%", "last 2 versions", "not ie <= 8"],
                //   },
                //   useBuiltIns: "usage",
                //   corejs: 3,
                // },
              ],
              "@babel/preset-react",
            ],
          },
        },
      },
      {
        test: /\.css$/,
        use: ["style-loader", "css-loader"],
      },
      // Add rules for other asset types as needed (e.g., images, fonts)
    ],
  },
  resolve: {
    fallback: {
      util: require.resolve("util/"),
      path: require.resolve("path-browserify"),
      url: require.resolve("url/"),
      vm: require.resolve("vm-browserify"),
      https: require.resolve("https-browserify"),
      http: require.resolve("stream-http"),
      buffer: require.resolve("buffer/"),
      stream: require.resolve("stream-browserify"),
      zlib: require.resolve("browserify-zlib"),
      assert: require.resolve("assert/"),
      constants: require.resolve("constants-browserify"),
      os: require.resolve("os-browserify/browser"),
      crypto: require.resolve("crypto-browserify"),
      querystring: require.resolve("querystring-es3"),
      tty: require.resolve("tty-browserify"),
      fs: false, // Disable the fs module
    },
    extensions: [".js", ".jsx"], // Add extensions for JSX and other file types
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: "./public/index.html",
      filename: "index.html",
    }),
  ],
};
