const path = require('path');
const webpack = require('webpack');
const HtmlWebpackPlugin = require('html-webpack-plugin');

var webpackConfig = require('./base.config.js');

webpackConfig.mode = 'development';

webpackConfig.devtool = 'source-map';

var pages = webpackConfig._pages;
for (var i = 0; i < pages.length; i++) {
    var page = pages[i];
    webpackConfig.entry[page.chunk] = page.js;

    webpackConfig.plugins.push(new HtmlWebpackPlugin({
        template: page.html,
        chunks: [page.chunk],
        filename: path.resolve(
            webpackConfig.output.path, 'build', page.chunk, 'index.html'
        )
    }));
}
delete webpackConfig._pages;

webpackConfig.devServer = {
    port: 8081,
    proxy: {
      '/api/*': {
        host: 'api.io',
        target: 'http://localhost:8080/',
        pathRewrite: {
          '/api' : ''
        }
      }
    }
  }

module.exports = webpackConfig;
