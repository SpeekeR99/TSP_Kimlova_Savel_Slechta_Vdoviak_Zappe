import * as path from 'path'
import webpack from 'webpack'
import { merge } from 'webpack-merge'
import commonConfig from './webpack.config'

module.exports = merge(commonConfig, {
	entry: [
		path.resolve(__dirname, './src/client/index.tsx'),
		'webpack-hot-middleware/client?quiet=true',
	],
	mode: 'development',
	devtool: 'source-map',
	plugins: [
		new webpack.HotModuleReplacementPlugin(),
		new webpack.NoEmitOnErrorsPlugin(),
	],
})
