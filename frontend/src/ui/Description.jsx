import styled from "styled-components";

export const Description = styled.div`
  max-width: 90rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;

  @media (max-width: 567.98px) {
    gap: 0.7rem;
  }

  font-size: 2rem;

  & span {
    font-size: 1.8rem;
    color: var(--color-grey-500);
  }
  & strong {
    font-weight: 500;
  }
  & a {
    display: inline-block;
    position: relative;
  }
  & a::before {
    content: "";
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 100%;
    height: 1px;
    background-color: var(--color-grey-700);
    transition: width 0.32s ease;
  }
  & a:hover::before {
    width: 0;
  }

  @media (max-width: 767.98px) {
    font-size: 1.8rem;
    strong {
      font-weight: 400;
    }
  }
  @media (max-width: 567.98px) {
    font-size: 1.6rem;
  }
  @media (max-width: 439.98px) {
    font-size: 1.4rem;
  }
`;
