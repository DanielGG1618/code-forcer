import styled, { css } from "styled-components";
import Input from "../../ui/Input.jsx";

export const StyledCover = styled.div`
  position: relative;
  max-width: 90rem;
  gap: 1rem;

  text-align: center;
  color: var(--color-grey-600);
  font-size: 1.6rem;
  font-weight: 500;
  padding: 3rem 4.5rem 5rem;
  transition: all 0.3s;
  box-shadow: var(--shadow-md);
  border-radius: var(--border-radius-md);

  @media (max-width: 567.98px) {
    margin-left: -2rem;
    margin-right: -2rem;
    padding: 2.5rem 2rem 0;
    border-top: 2px solid var(--color-grey-200);
    border-radius: 0;
    box-shadow: none;
  }
`;

export const ButtonBack = styled.button`
  position: absolute;
  left: 2rem;
  top: 2rem;
  background-color: transparent;
  border: none;

  svg {
    width: 5rem;
    height: 5rem;
    transition: fill 0.3s ease;

    @media (max-width: 479.98px) {
      width: 3rem;
      height: 3rem;
    }
  }
  &:hover svg {
    fill: var(--color-brand-600);
  }

  @media (max-width: 399.98px) {
    display: none;
  }
`;

export const Description = styled.div`
  display: flex;
  justify-content: center;

  &:not(:last-child) {
    margin-bottom: 3.5rem;
  }
`;

export const List = styled.form`
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 3rem;

  > button {
    align-self: center;
    padding-left: 8rem;
    padding-right: 8rem;
  }
`;
export const Item = styled.div`
  position: relative;
  display: flex;
  flex-direction: column;
  padding: 3rem 4rem;
  column-gap: 0.8rem;
  border-radius: var(--border-radius-md);
  border: 2px solid var(--color-grey-200);

  @media (max-width: 479.98px) {
    padding-left: 2rem;
    padding-right: 2rem;
  }

  font-weight: 400;

  strong {
    font-weight: 500;
  }

  > strong {
    font-size: 2rem;
  }
  > strong:not(:last-child) {
    margin-bottom: 1.5rem;
  }
  > input:not(:last-child) {
    margin-bottom: 0.2rem;
  }

  ${(props) =>
    parseInt(props.undefined) > 0 &&
    css`
      border: 1px solid var(--color-yellow-700);
    `}
`;

export const ItemRow = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 2.5rem;
  margin-top: 2rem;

  span {
    display: inline-flex;
    align-items: center;
    gap: 1rem;
  }
  span strong {
    align-self: flex-start;
    font-size: 2rem;
    padding-bottom: 0.3rem;
  }

  @media (max-width: 767.98px) {
    gap: 1.5rem;
  }
  @media (max-width: 567.98px) {
    flex-direction: column;
    span {
      font-size: 1.4rem;
    }
    span strong {
      font-size: 1.6rem;
    }
  }
`;

export const ItemInput = styled(Input)`
  max-width: 20rem;
  margin: 0 auto;
  text-align: center;
  padding: 0.3rem 1rem;
  font-size: 1.4rem;

  &:not(:last-child) {
    margin-bottom: 0.5rem;
  }
`;

export const Error = styled.span`
  font-size: 1.4rem;
  color: var(--color-red-700);
`;

export const UndefinedUsersList = styled.div`
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  row-gap: 0.6rem;
  column-gap: 1.2rem;
  margin-top: 2rem;

  @media (max-width: 567.98px) {
    font-size: 1.4rem;
  }

  & span {
    position: relative;
    display: inline-flex;
    align-items: center;
    gap: 0.6rem;
  }
  & span::before {
    content: "";
    flex: 0 0 0.3rem;
    width: 0.3rem;
    height: 0.3rem;
    border-radius: 100%;
    background-color: var(--color-grey-700);
  }
`;

export const UndefinedDescription = styled.p`
  padding: 2rem 2.5rem;
  border: 2px solid var(--color-red-400);
  border-radius: var(--border-radius-md);

  font-weight: 400;
  b {
    font-weight: 500;
  }
  a {
    font-weight: 500;
    text-decoration: underline;
  }
`;

export const LateSubmissionsContainer = styled.div`
  max-width: 60rem;
  margin-left: auto;
  margin-right: auto;
  margin-top: 2rem;
  margin-bottom: 2rem;

  h2:not(:last-child) {
    margin-bottom: 2.5rem;
  }
  h3:not(:last-child) {
    margin-bottom: 1rem;
  }
`;

export const TimeConfiguration = styled.div`
  display: grid;
  grid-template-columns: repeat(3, 10rem);
  column-gap: 2rem;
  row-gap: 1rem;

  &:not(:last-child) {
    margin-bottom: 1rem;

    @media (max-width: 567.98px) {
      margin-bottom: 2rem;
    }
  }

  @media (max-width: 567.98px) {
    grid-template-columns: repeat(3, 5rem);
    justify-content: center;
    > label > input {
      padding: 0.8rem;
    }
    > label > input + span {
      top: 1rem;
      background-color: transparent;
      left: 50%;
      transform: translateX(-50%);
      color: var(--color-grey-500);
      transition: color 0.3s ease;
    }
    > label > input:focus ~ span {
      transform: translateX(-50%);
      color: var(--color-grey-700);
    }
  }
`;

export const SubmissionsAction = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 2rem;

  > div {
    flex: 0 0 25rem;
  }

  @media (max-width: 567.98px) {
    flex-direction: column;

    > * {
      width: 100%;
    }
    > div {
      flex: auto;
    }
  }
`;
