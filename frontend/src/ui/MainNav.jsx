import styled from "styled-components";
import { NavLink } from "react-router-dom";
import { HiHome } from "react-icons/hi2";
import { SiCodeforces } from "react-icons/si";
import { FaDatabase } from "react-icons/fa6";
import { useEffect, useState } from "react";

const StyledNav = styled.nav`
  @media (max-width: 767.98px) {
    position: fixed;
    padding: 0.4rem 2rem;
    z-index: 1;
    bottom: 0;
    left: 0;
    right: 0;
    border-top: 1px solid var(--color-grey-100);
    background-color: var(--color-grey-0);
  }
`;

const NavList = styled.ul`
  display: flex;
  flex-direction: column;
  gap: 0.8rem;

  @media (max-width: 991.98px) {
    flex-direction: row;
    flex-wrap: wrap;
  }
  @media (max-width: 767.98px) {
    justify-content: center;
  }
`;

const StyledNavLink = styled(NavLink)`
  &:link,
  &:visited {
    display: flex;
    align-items: center;
    gap: 1.2rem;

    color: var(--color-grey-600);
    font-size: 1.6rem;
    font-weight: 500;
    padding: 1.2rem 2.4rem;
    transition: all 0.3s;
  }

  &:hover,
  &:active,
  &.active:link,
  &.active:visited {
    color: var(--color-grey-800);
    background-color: var(--color-grey-50);
    border-radius: var(--border-radius-sm);
  }

  & svg {
    flex: 0 0 2.4rem;
    width: 2.4rem;
    height: 2.4rem;
    color: var(--color-grey-400);
    transition: all 0.3s;
  }

  &:hover svg,
  &:active svg,
  &.active:link svg,
  &.active:visited svg {
    color: var(--color-brand-500);
  }

  @media (max-width: 991.98px) {
    &:link,
    &:visited {
      align-items: flex-end;
      gap: 0.8rem;
      line-height: 1.3;
      font-size: 1.4rem;
      padding: 1rem 1.5rem;
    }
    & svg {
      flex: 0 0 2rem;
      width: 2rem;
      height: 2rem;
    }
  }
  @media (max-width: 439.98px) {
    &:link,
    &:visited {
      gap: 0.4rem;
      padding: 1rem 1.2rem;
      font-size: 1.2rem;
    }
    & svg {
      flex: 0 0 1.6rem;
      width: 1.6rem;
      height: 1.6rem;
    }
  }
`;

function MainNav() {
  const [userIsDesktop, setUserIsDesktop] = useState(true);
  useEffect(() => {
    window.innerWidth > 530 ? setUserIsDesktop(true) : setUserIsDesktop(false);
  }, [userIsDesktop]);
  return (
    <StyledNav>
      <NavList>
        <li>
          <StyledNavLink to="/">
            <HiHome />
            <span>Home</span>
          </StyledNavLink>
        </li>
        <li>
          <StyledNavLink to="/contests">
            <SiCodeforces />
            <span>{userIsDesktop && "Download"} Submissions</span>
          </StyledNavLink>
        </li>
        <li>
          <StyledNavLink to="/handles">
            <FaDatabase />
            <span>{userIsDesktop && "Edit"} Handles</span>
          </StyledNavLink>
        </li>
      </NavList>
    </StyledNav>
  );
}

export default MainNav;
