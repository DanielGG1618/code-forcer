import styled, { css } from "styled-components";

const StyledLabel = styled.label`
  display: block;
  position: relative;
  padding-top: 2.7rem;

  & > input,
  & > label > span {
    padding-top: 1.3rem;
    padding-bottom: 1.3rem;
  }
  & > input {
    width: 100%;
  }
  & > input + input {
    margin-top: 1.4rem;
  }
  &:not(:last-child) {
    padding-bottom: 2rem;
    border-bottom: 1px solid var(--color-grey-100);
  }
  input:focus ~ span {
    transform: translate(0, -1.6rem) scale(1.1);
  }
  input:disabled ~ span {
    background-color: var(--color-grey-200);
    border-color: var(--color-grey-300);
  }

  ${(props) =>
    props.borderless === true &&
    css`
      &:not(:last-child) {
        padding-bottom: 0;
        border-bottom: none;
      }
    `}

  ${(props) =>
    props.type === "file" &&
    css`
      &:hover > span {
        transform: translate(0, -1.6rem) scale(1.1);
      }
    `}

  ${(props) =>
    props.text !== undefined &&
    css`
      display: grid;
      column-gap: 1.5rem;

      span:last-child {
        grid-row: 2;
        grid-column: span 2;
      }
    `}
`;
const StyledSpan = styled.span`
  position: absolute;
  top: 1.6rem;
  left: 1rem;
  padding: 0 0.5rem;
  background-color: var(--color-grey-0);
  border-radius: var(--border-radius-md);
  border: 1px solid transparent;

  font-size: 1.5rem;
  line-height: 1.1;
  transition: transform 0.3s ease;

  @media (max-width: 567.98px) {
    top: 2rem;
    font-size: 1.3rem;
  }
`;

const ErrorMessage = styled.span`
  position: static !important;
  transform: none !important;
  display: inline-block;
  font-size: 1.4rem;
  color: var(--color-red-700);
  margin-top: 0.6rem;
`;

const StyledText = styled.div`
  align-self: center;
  grid-column: 2;
  @media (max-width: 479.98px) {
    font-size: 1.3rem;
  }
`;

function FormElement({
  label,
  children,
  type = "",
  error,
  text,
  borderless = false,
}) {
  return (
    <StyledLabel type={type} text={text} borderless={borderless}>
      {children}
      <StyledSpan>{label}</StyledSpan>
      {text && <StyledText>{text}</StyledText>}
      {error && <ErrorMessage>{error}</ErrorMessage>}
    </StyledLabel>
  );
}

export default FormElement;
