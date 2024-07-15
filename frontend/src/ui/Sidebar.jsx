import styled from "styled-components";
import Logo from "./Logo.jsx";
import MainNav from "./MainNav.jsx";
import ThemeButton from "./ThemeButton.jsx";

const StyledSwitch = styled(ThemeButton)`
  max-width: none;
`;

const StyledSidebar = styled.aside`
  grid-row: 1 / -1;
  display: flex;
  flex-direction: column;
  gap: 3.2rem;
  padding: 3.2rem 2.4rem;
  border-right: 1px solid var(--color-grey-100);
  background-color: var(--color-grey-0);
  overflow-y: auto;

  @media (max-width: 991.98px) {
    border-right: none;
    border-bottom: 1px solid var(--color-grey-100);
    grid-row: 1;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    padding: 0 2rem;
  }
`;

function Sidebar() {
  return (
    <StyledSidebar>
      <Logo />
      <MainNav />
      <StyledSwitch align={"center"} />
    </StyledSidebar>
  );
}

export default Sidebar;
