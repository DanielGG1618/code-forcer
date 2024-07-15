import styled from "styled-components";
import { NavLink } from "react-router-dom";

const StyledCard = styled(NavLink)`
  &:link,
  &:visited {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1.8rem;

    text-align: center;
    color: var(--color-grey-600);
    font-size: 1.6rem;
    font-weight: 500;
    padding: 1.2rem 2.4rem 2rem 2.4rem;
    transition: all 0.3s;
    box-shadow: var(--shadow-md);
    border-radius: var(--border-radius-tiny);
  }

  &:hover,
  &:active,
  &.active:link,
  &.active:visited {
    color: var(--color-grey-800);
    background-color: var(--color-grey-100);
    border-radius: var(--border-radius-lg);
  }

  & svg {
    flex: 0 0 10rem;
    width: 10rem;
    height: 10rem;
    transition: all 0.3s ease;
    margin-bottom: auto;
    color: var(--color-brand-500);
  }

  & span {
    font-weight: 500;
    font-size: 2.4rem;
  }

  @media (max-width: 767.98px) {
    gap: 0.2rem;
    & svg {
      flex: 0 0 8rem;
      width: 8rem;
      height: 8rem;
    }
    & span {
      font-size: 1.9rem;
    }
  }
  @media (max-width: 567.98px) {
    & svg {
      flex: 0 0 6rem;
      width: 6rem;
      height: 6rem;
    }
    span {
      font-size: 1.6rem;
    }
  }
`;

function Card({ title, icon, to }) {
  return (
    <StyledCard to={to}>
      {icon()}
      <span>{title}</span>
    </StyledCard>
  );
}

export default Card;
