const path = require("path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = (env) => {
  return {
    entry: {
      status: ["./src/scss/status.scss"],
      mgmt: ["./src/scss/mgmt.scss"],
      report_form: ["./src/js/report_form.js"],
      reports: ["./src/js/reports.js"],
    },
    output: {
      filename: "[name].js",
      path: path.resolve(__dirname, "static"),
    },
    mode: env.production ? "production" : "development",
    module: {
      rules: [
        {
          test: /\.scss$/,
          use: [
            // fallback to style-loader in development
            !env.production ? "style-loader" : MiniCssExtractPlugin.loader,
            "css-loader",
            "sass-loader",
          ],
        },
        {
          test: /\.m?js$/,
          exclude: /(node_modules|bower_components)/,
          use: {
            loader: "babel-loader",
            options: {
              presets: ["@babel/preset-env"],
            },
          },
        },
      ],
    },
    plugins: [
      new MiniCssExtractPlugin({
        filename: "[name].css",
      }),
    ],
  };
};
