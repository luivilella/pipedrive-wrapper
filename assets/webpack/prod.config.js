const webpack = require('webpack');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const path = require('path');
const WebpackStrip = require('strip-loader');
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');

var webpackConfig = require('./base.config.js');

webpackConfig.output.filename = 'build/[name]/[hash]/bundle.js';

webpackConfig.optimization.minimizer.push(
    new UglifyJsPlugin({
        cache: true,
        parallel: true,
        uglifyOptions: {
            compress: false,
            ecma: 6,
            mangle: true
        },
        sourceMap: false
    })
)

webpackConfig.mode = 'production';

var pages = webpackConfig._pages;
for (var i = 0; i < pages.length; i++) {
    var page = pages[i];
    webpackConfig.entry[page.chunk] = page.js;

    webpackConfig.plugins.push(new HtmlWebpackPlugin({
        template: page.html,
        chunks: [page.chunk],
        filename: path.resolve(
            webpackConfig.output.path, 'build', page.chunk, 'index.html'
        ),
        minify: {
            collapseWhitespace: true,
            preserveLineBreaks: false
        }
    }));
}
delete webpackConfig._pages;

webpackConfig.module.rules.push({
    test: /\.js$/,
    exclude: /(node_modules|bower_components)/,
    loader: WebpackStrip.loader('console.log', 'debugger')
});

webpackConfig.output.publicPath = '/assets/';

module.exports = webpackConfig;
