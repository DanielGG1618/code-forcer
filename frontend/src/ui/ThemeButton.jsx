import { useDarkMode } from "../context/DarkModeContext.jsx";
import styled, { css } from "styled-components";

const themes = {
  light: css`
    background-color: var(--color-brand-900);
  `,
  dark: css`
    background-color: var(--color-grey-600);
  `,
};

const StyledLabel = styled.label`
  ${(props) => (props.align ? "align-self: center" : "")};
  cursor: pointer;
  max-width: max-content;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.8rem 2rem;
  border-radius: 50rem;
  ${(props) => themes[props.theme]}
`;

const StyledInput = styled.input`
  display: none;

  & + div {
    border-radius: 50%;
    width: 2rem;
    height: 2rem;
    position: relative;
    box-shadow: inset 0.65rem -0.65rem 0 0 var(--color-brand-600, #000);
    transform: scale(1) rotate(-2deg);
    transition:
      box-shadow 0.5s ease 0s,
      transform 0.4s ease 0.1s;
  }
  & + div::before {
    content: "";
    width: inherit;
    height: inherit;
    border-radius: inherit;
    position: absolute;
    left: 0;
    top: 0;
    transition: background 0.3s ease;
  }
  & + div::after {
    content: "";
    width: 0.3rem;
    height: 0.3rem;
    border-radius: 50%;
    margin: -2px 0 0 -2px;
    position: absolute;
    top: 50%;
    left: 50%;
    box-shadow:
      0 -13px 0 var(--color-grey-100, #eee),
      0 13px 0 var(--color-grey-100, #eee),
      13px 0 0 var(--color-grey-100, #eee),
      -13px 0 0 var(--color-grey-100, #eee),
      9px 9px 0 var(--color-grey-100, #eee),
      -9px 9px 0 var(--color-grey-100, #eee),
      9px -9px 0 var(--color-grey-100, #eee),
      -9px -9px 0 var(--color-grey-100, #eee);
    transform: scale(0);
    transition: all 0.3s ease;
  }
  &:checked + div {
    box-shadow: inset 32px -32px 0 0 #fff;
    transform: scale(0.5) rotate(0deg);
    transition:
      transform 0.3s ease 0.1s,
      box-shadow 0.2s ease 0s;
  }
  &:checked + div::before {
    background: var(--color-grey-100, #eee);
    transition: background 0.3s ease 0.1s;
  }
  &:checked + div::after {
    transform: scale(1.5);
    transition: transform 0.5s ease 0.15s;
  }
`;

function ThemeButton({ align }) {
  const { isDarkMode, toggleDarkMode } = useDarkMode();

  return (
    <StyledLabel
      align={align}
      theme={isDarkMode ? "dark" : "light"}
      title={isDarkMode ? "Activate light mode" : "Activate dark mode"}
      aria-label={isDarkMode ? "Activate light mode" : "Activate dark mode"}
    >
      <StyledInput
        type="checkbox"
        defaultChecked={!isDarkMode}
        onChange={toggleDarkMode}
      />
      <div />
    </StyledLabel>
  );
}

export default ThemeButton;
