import adapter from '@sveltejs/adapter-static';

const config = { 
  kit: { 
    adapter: adapter({
      pages: 'build',
      assets: 'build',
      fallback: 'index.html',
      precompress: false,
      strict: true
    }),
    prerender: {
      handleHttpError: 'warn'
    }
  } 
};

export default config;
