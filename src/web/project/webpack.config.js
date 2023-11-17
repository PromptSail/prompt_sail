import { resolve } from 'path';
import { ProvidePlugin } from "webpack";
export const mode = 'development';
export const output = {
  path: resolve(__dirname, 'dist'),
  filename: 'main.min.js',
};
export const devtool = 'eval-source-map';
export const module = {
  rules: [
    {
      test: /\.js$/,
      exclude: /(node_modules)/,
      use: {
        loader: 'babel-loader',
        options: {
          presets: ['@babel/preset-env'],
        },
      },
    },
    {
      test: /\.s[ac]ss$/i,
      use: ['style-loader', 'css-loader', 'sass-loader'],
    },
  ],
};
export const plugins = [
  new ProvidePlugin({
    jQuery: 'jquery',
    $: 'jquery',
    'window.jQuery': 'jquery',
  }),
];
