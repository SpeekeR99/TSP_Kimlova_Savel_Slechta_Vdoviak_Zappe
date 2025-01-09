import * as path from 'path'
import HtmlWebpackPlugin from 'html-webpack-plugin'
import CopyWebpackPlugin from 'copy-webpack-plugin'
import { Configuration } from 'webpack'

const config: Configuration = {
	entry: path.resolve(__dirname, './dist/src/client/index.js'),
	devtool: false,
	module: {
		rules: [
			{
				test: /\.tsx?$/,
				use: 'ts-loader',
				exclude: /node_modules/,
			},
		],
	},
	mode: 'production',
	target: 'web',
	resolve: {
		extensions: ['.tsx', '.ts', '.js'],
	},
	output: {
		path: path.resolve(__dirname, './dist'),
		publicPath: '/',
		filename: '[name].js',
	},
	plugins: [
		new HtmlWebpackPlugin({
			filename: 'index.html',
			template: path.resolve(__dirname, './src/client/public/index.html'),
		}),
		new CopyWebpackPlugin({
			patterns: [
				{
					from: path.resolve(__dirname, './src/client/public/garbage.ico'),
					to: path.resolve(__dirname, './dist/garbage.ico'),
				},
			],
		}),
	],
	performance: {
		hints: false,
		maxEntrypointSize: 512000,
		maxAssetSize: 512000,
	},
}

export default config
