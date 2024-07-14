import { Outlet, useNavigation } from "react-router-dom";
import styled from "styled-components";
import Sidebar from "./Sidebar.jsx";
import FullPage from "./FullPage.jsx";
import Spinner from "./Spinner.jsx";

const StyledAppLayout = styled.div`
  display: grid;
  grid-template-columns: 28rem 1fr;
  height: 100dvh;
  @media (max-width: 991.98px) {
    grid-template-columns: 1fr;
    grid-template-rows: 10rem 1fr;
  }
  @media (max-width: 767.98px) {
    grid-template-rows: 6rem 1fr 4.5rem;
  }
  @media (max-width: 438.98px) {
    grid-template-rows: 6rem 1fr 3.7rem;
  }
`;
const Main = styled.main`
  position: relative;
  background-color: var(--color-grey-50);
  padding: 4rem 4.8rem 6.4rem;
  overflow-y: auto;
  transition: opacity 0.5s ease;

  @media (max-width: 1199.98px) {
    padding-right: 2rem;
    padding-left: 2rem;
  }
`;

const Container = styled.div`
  min-height: 100%;
  max-width: 120rem;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 3.2rem;
`;

function AppLayout() {
  const navigation = useNavigation();
  return (
    <StyledAppLayout>
      <Sidebar />
      <Main>
        {navigation.state === "loading" && (
          <FullPage>
            <Spinner />
          </FullPage>
        )}
        <Container>
          <Outlet />
        </Container>
      </Main>
    </StyledAppLayout>
  );
}

export default AppLayout;
