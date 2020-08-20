const BundleTracker = require("webpack-bundle-tracker");
const paths = require("react-scripts/config/paths");
const WriteFilePlugin = require("write-file-webpack-plugin");
const {
  override,
  addWebpackPlugin,
} = require("customize-cra");

function appOverride(config) {
  const bucket = `https://storage.googleapis.com/${process.env.REACT_GCLOUD_BUCKET}/`;
  config.optimization.splitChunks.name = "vendor";
  config.optimization.runtimeChunk = false;
  config.output.futureEmitAssets = false;
  config.output.path = paths.appBuild;
  config.output.publicPath = config.mode === "production" ? bucket : config.output.publicPath;
  return config;
}

module.exports = override(
  appOverride,
  addWebpackPlugin(
    new BundleTracker({ filename: "./build/webpack-stats.json" })
  ),
  addWebpackPlugin(new WriteFilePlugin())
);
