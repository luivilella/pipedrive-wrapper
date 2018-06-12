const webpack = require('webpack');
const path = require('path');
const fs = require('fs');

const PATH_BASE = path.resolve(__dirname, '..');
const PATH_PAGES = path.resolve(PATH_BASE, 'src', 'pages');


var config = {
    _pages: [
        {
            chunk: 'search',
            html: path.resolve(PATH_PAGES, 'search', 'page.html'),
            js: path.resolve(PATH_PAGES, 'search', 'page.js'),
        },
        {
            chunk: 'organization-create',
            html: path.resolve(PATH_PAGES, 'organization-create', 'page.html'),
            js: path.resolve(PATH_PAGES, 'organization-create', 'page.js'),
        },
        {
            chunk: 'organization-detail',
            html: path.resolve(PATH_PAGES, 'organization-detail', 'page.html'),
            js: path.resolve(PATH_PAGES, 'organization-detail', 'page.js'),
        },
    ],
    entry: {},
    output: {
        path: path.resolve(PATH_BASE, 'dist'),
        filename: 'build/[name]/bundle.js'
    },
    resolve: {
        alias: {
            vue: 'vue/dist/vue.esm.js'
        },
        modules: [
            path.resolve(PATH_BASE, 'src'),
            path.resolve(PATH_BASE, 'node_modules'),
        ]
    },
    plugins: [
        new webpack.LoaderOptionsPlugin({ options: {} }),
    ],
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /(node_modules|bower_components)/,
                enforce: 'pre',
                loader: 'jshint-loader'
            },
            {
                test: /\.js$/,
                exclude: /(node_modules|bower_components)/,
                loader: 'babel-loader'
            },
            {
                test: /\.css$/,
                use: [
                    'style-loader',
                    'css-loader'
                ]
            },
            {
                test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/,
                loader: 'url-loader?limit=10000&mimetype=application/font-woff'
            },
            {
                test: /\.(jpe?g|png|gif|ttf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/,
                loader: 'file-loader'
            },
        ]
    },
    optimization: {
        minimizer: []
    }
};

module.exports = config;
