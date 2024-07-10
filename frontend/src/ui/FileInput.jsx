import styled, { css } from "styled-components";

const FileInputElement = styled.input.attrs({ type: "file" })`
  display: none;
`;
const FileInputLabel = styled.label`
  cursor: pointer;
  display: flex;
  align-self: center;
  gap: 2rem;

  border: 1px solid var(--color-grey-300);
  border-radius: var(--border-radius-sm);
  background-color: var(--color-grey-0);
  box-shadow: var(--shadow-sm);

  font-size: 1.4rem;

  // &:hover {
  //   background-color: var(--color-grey-100);
  // }
  &:focus {
    outline: 2px solid var(--color-brand-600);
    outline-offset: -1px;
  }

  ${(props) =>
    props.edited === "true" &&
    css`
      & span {
        opacity: 1;
      }
    `}
`;
const FileInputText = styled.span`
  opacity: 0.6;
  flex: 1 1 auto;
  padding: 0.8rem 1.2rem;
`;
const FileInputButton = styled.span`
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.8rem 2.6rem;
  color: var(--color-brand-50);
  border-radius: 0 var(--border-radius-sm) var(--border-radius-sm) 0;
  background-color: var(--color-brand-600);

  &:hover:not(:disabled) {
    background-color: var(--color-brand-700);
  }
`;

function FileInput({ edited, text, register, accept }) {
  return (
    <FileInputLabel edited={edited}>
      <FileInputText>{text}</FileInputText>
      <FileInputElement accept={accept} {...register} />
      <FileInputButton>Browse</FileInputButton>
    </FileInputLabel>
  );
}

export default FileInput;
