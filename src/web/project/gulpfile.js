import gulp from 'gulp';
import dartSass from 'sass';
import gulpSass from 'gulp-sass';
import rename from 'gulp-rename';
import cssmin from 'gulp-cssnano';
import prefix from 'gulp-autoprefixer';
import uglify from 'gulp-uglify';
import imagemin from 'gulp-imagemin';
import pug from 'gulp-pug';
import browserSync from 'browser-sync';
import { deleteAsync } from 'del';
import prettier from 'gulp-prettier';
import eslint from 'gulp-eslint';
import webpack from 'webpack-stream';
const sass = gulpSass(dartSass);

const pugDir = '../templates';
const cssDir = '../../../static/css';
const jsDir = '../../../static/js';

const staticPath = {
    js: '/static/js',
    css: '/static/css'
};

const format = () => {
    return (
        gulp
            .src(['src/**/*.ts'])
            .pipe(prettier.check('.prettierrc'))
            // .pipe(eslint())
            .pipe(eslint.format())
            .pipe(eslint.failAfterError())
    );
};

function pugCompile() {
    return gulp
        .src('src/pages/*.pug')
        .pipe(
            pug({
                basedir: `/src`,
                pretty: true,
                locals: { staticPath }
            })
        )
        .pipe(gulp.dest(pugDir))
        .pipe(browserSync.stream());
}

function sassCompile() {
    return (
        gulp
            .src('src/main.sass')
            .pipe(sass())
            .pipe(prefix())
            // .pipe(cssmin())
            .pipe(rename('main.min.css'))
            .pipe(gulp.dest(cssDir))
    );
}

function tsCompile() {
    return (
        gulp
            .src('src/main.ts')
            .pipe(
                webpack({
                    mode: 'development',
                    module: {
                        rules: [
                            {
                                test: /\.ts$/,
                                exclude: /(node_modules)/,
                                use: 'ts-loader'
                            }
                        ]
                    },
                    resolve: {
                        extensions: ['.tsx', '.ts', '.js']
                    }
                })
            )
            // .pipe(uglify())
            .pipe(gulp.dest(jsDir))
    );
}

function copyAssets() {
    return gulp.src('src/assets/images/**/*').pipe(gulp.dest(cssDir));
}

function minifyImages() {
    return gulp.src('src/assets/images/*').pipe(imagemin()).pipe(gulp.dest(cssDir));
}

function bsServe(done) {
    browserSync.init({
        proxy: 'http://localhost:8000',
        // server: {
        //   baseDir: pugDir,
        //   directory: true,
        // },
        ui: {
            proxy: 'http://localhost:8000'
        }
    });
    done();
}

function bsReload(done) {
    browserSync.reload();
    done();
}

function fileWatch() {
    gulp.watch('src/**/*.pug', gulp.series(pugCompile, bsReload));
    gulp.watch('src/**/*.s?(a|c)ss', gulp.series(sassCompile, bsReload));
    gulp.watch('src/**/*.ts', gulp.series(tsCompile, bsReload));
    gulp.watch('src/assets/**/*', gulp.series(copyAssets, bsReload));
    gulp.watch('src/**/*.json', gulp.series(tsCompile, bsReload));
}

function cleanBuild() {
    return deleteAsync([`${pugDir}/*`, `${cssDir}/*`, `${jsDir}/*`], { force: true });
}

const commonSeries = gulp.series(
    format,
    cleanBuild,
    pugCompile,
    sassCompile,
    tsCompile,
    copyAssets
);
const dev = () => gulp.series(commonSeries, bsServe, fileWatch);

gulp.task('dev', dev());
