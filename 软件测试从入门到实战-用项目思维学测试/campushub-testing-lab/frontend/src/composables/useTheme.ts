import { ref } from 'vue'

export type ThemeMode = 'light' | 'dark'

export function useTheme() {
  const theme = ref<ThemeMode>('light')

  function initTheme() {
    const savedTheme = localStorage.getItem('campushub-theme')
    theme.value = savedTheme === 'dark' ? 'dark' : 'light'
    document.documentElement.dataset.theme = theme.value
  }

  function toggleTheme() {
    theme.value = theme.value === 'light' ? 'dark' : 'light'
    document.documentElement.dataset.theme = theme.value
    localStorage.setItem('campushub-theme', theme.value)
  }

  return {
    theme,
    initTheme,
    toggleTheme
  }
}
