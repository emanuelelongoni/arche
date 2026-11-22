// Applies a remembered theme before first paint. Inline (so it runs before the page
// renders) and shared with astro.config.mjs, which adds its hash to the CSP.
export const THEME_INIT =
  'try{var t=localStorage.getItem("arche-theme");if(t==="light"||t==="dark")document.documentElement.dataset.theme=t}catch(e){}';
