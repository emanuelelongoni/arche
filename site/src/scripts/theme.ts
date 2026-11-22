// The footer's System / Light / Dark control. The choice is kept on this device only.
const KEY = "arche-theme";

function stored(): string {
  try {
    return localStorage.getItem(KEY) ?? "system";
  } catch {
    return "system";
  }
}

function apply(choice: string) {
  const root = document.documentElement;
  if (choice === "light" || choice === "dark") root.dataset.theme = choice;
  else delete root.dataset.theme;
}

export function initThemeControl() {
  const control = document.querySelector<HTMLFieldSetElement>("[data-theme-control]");
  if (!control) return;
  const current = stored();
  for (const input of control.querySelectorAll<HTMLInputElement>("input[name=theme]")) {
    input.checked = input.value === current;
    input.addEventListener("change", () => {
      apply(input.value);
      try {
        if (input.value === "system") localStorage.removeItem(KEY);
        else localStorage.setItem(KEY, input.value);
      } catch {
        /* storage unavailable: the choice lasts for this page only */
      }
    });
  }
  control.hidden = false;
}
