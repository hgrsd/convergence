const path = require("path");

module.exports = {
	entry: ["./src/index.jsx", "./style/index.scss"],
	output: {
		filename: "app.js",
		path: path.resolve(__dirname, "dist")
	},
	resolve: {
		extensions: [".js", ".jsx"]
	},
	mode: "production",
	module: {
		rules: [{
			test: /\.scss$/,
			use: [{
				loader: "file-loader",
				options: {
					name: "[name].css",
				}
			}, {
				loader: "extract-loader"
			}, {
				loader: "css-loader"
			}, {
				loader: "sass-loader"
			}]
		}, {
			test: /.jsx?$/,
			exclude: /node_modules/,
			use: {
				loader: "babel-loader",
				options: {
					presets: ["@babel/preset-env", "@babel/preset-react"]
				}
			}
		}]
	}
};