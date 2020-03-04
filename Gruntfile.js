module.exports = function(grunt) {
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    sass: {
      options: {
          loadPath: ['recourse/assets/vendor/govuk-frontend/src']
        },
      dist: {
        files: {
          'recourse/static/css/main.css' : 'recourse/assets/scss/main.scss'
        }
      }
    },
    cssmin: {
      target: {
        files: [{
          expand: true,
          cwd: 'recourse/static/css/',
          src: ['*.css', '!*.min.css'],
          dest: 'recourse/static/css/',
          ext: '.min.css'
        }]
      }
    },
    copy: {
      target: {
        files: [
          {
            expand: true,
            cwd: 'recourse/assets/javascript',
            src: ['*.js'],
            dest: 'recourse/static/javascript',
            filter: 'isFile'
          },          
          {
            expand: true,
            cwd: 'recourse/assets/images',
            src: ['*.png', '*.jpg', '*.svg'],
            dest: 'recourse/static/images',
            filter: 'isFile'
          },
          {
            expand: true,
            cwd: 'recourse/assets/fonts',
            src: ['**/*.css', '**/*.woff', '**/*.eot', '**/*.woff2', '**/*.ttf', '**/*.svg', '**/*.svg', '**/*.rtf'],
            dest: 'recourse/static/fonts',
            filter: 'isFile'
          },
          {
            expand: true,
            cwd: 'recourse/assets/vendor/foundation-sites/dist',
            src: ['**/*.js'], 
            dest: 'recourse/static/vendor/foundation-sites', 
            filter: 'isFile'
          },
          {
            expand: true,
            cwd: 'recourse/assets/vendor/jquery/dist',
            src: ['**/*.js'], 
            dest: 'recourse/static/vendor/jquery', 
            filter: 'isFile'
          },
          {
            expand: true,
            cwd: 'recourse/assets/vendor/govuk-frontend/dist',
            src: ['**/*.js', '**/*.css'], 
            dest: 'recourse/static/vendor/govuk-frontend', 
            filter: 'isFile'
          }

        ]
      }
    },
    watch: {
      css: {
        files: '**/*.scss',
        tasks: ['sass', 'cssmin']
      },
      scripts: {
        files: 'recourse/assets/**/*.js',
        tasks: ['copy']
      },
    }
  });
  grunt.loadNpmTasks('grunt-contrib-sass');
  grunt.loadNpmTasks('grunt-contrib-cssmin');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-copy')
  grunt.registerTask('default',['watch']);
}
