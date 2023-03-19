/*
    Loads boostrap colours into a js dictionary 
*/

const style = window.getComputedStyle(document.documentElement);
const theme = {
    primary: style.getPropertyValue('--bs-primary'),
    secondary: style.getPropertyValue('--bs-secondary'),
    success: style.getPropertyValue('--bs-success'),
    info: style.getPropertyValue('--bs-info'),
    warning: style.getPropertyValue('--bs-warning'),
    danger: style.getPropertyValue('--bs-danger'),
    light: style.getPropertyValue('--bs-light'),
    dark: style.getPropertyValue('--bs-dark'),
};