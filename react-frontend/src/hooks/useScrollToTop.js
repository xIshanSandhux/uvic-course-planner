import { useEffect } from 'react';

export default function useScrollToTop() {
  useEffect(() => {
    // Prevent browser from restoring previous scroll position
    if ('scrollRestoration' in window.history) {
      window.history.scrollRestoration = 'manual';
    }

    // Scroll to top when the page mounts
    window.scrollTo({ top: 0, behavior: 'auto' });
  }, []);
}
