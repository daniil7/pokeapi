// webpack.config.js
const path = require('path')
const { CleanWebpackPlugin } = require('clean-webpack-plugin')

module.exports = {
    entry: {
        main: path.resolve(__dirname, './app/src/js/app.js'),
    },
    output: {
        path: path.resolve(__dirname, './app/static/build'),
        filename: 'bundle.js',
    },
    plugins: [
        new CleanWebpackPlugin(),
    ],
    module: {
        rules: [
            {
                test: /\.css$/i,
                include: path.resolve(__dirname, './app/src/css'),
                use: ['style-loader', 'css-loader', 'postcss-loader'],
            },
        ],
    },
    watchOptions: {
        aggregateTimeout: 0,
        poll: 1000,
    },
}
