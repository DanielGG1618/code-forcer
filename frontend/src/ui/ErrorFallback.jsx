import styled from "styled-components";
import GlobalStyles from "../styles/GlobalStyles.js";
import Button from "./Button.jsx";
import Heading from "./Heading.jsx";
import { useRouteError } from "react-router-dom";
import { useMoveBack } from "../hooks/useMoveBack.js";

const StyledErrorFallback = styled.div`
  height: 100vh;
  background-color: var(--color-grey-50);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 4.8rem;
  overflow: hidden;

  @media (max-width: 567.98px) {
    padding: 4.8rem 2rem;
  }
`;

const Box = styled.div`
  /* Box */
  background-color: var(--color-grey-0);
  border: 1px solid var(--color-grey-100);
  border-radius: var(--border-radius-md);

  padding: 4.8rem;
  flex: 0 1 96rem;
  text-align: center;

  @media (max-width: 567.98px) {
    padding: 4.8rem 2rem;
  }

  & h1 {
    margin-bottom: 1.6rem;
  }

  & p {
    font-family: "Sono", sans-serif;
    margin-bottom: 3.2rem;
    color: var(--color-grey-500);
  }
`;

function ErrorFallback() {
  const error = useRouteError();
  const moveBack = useMoveBack();

  return (
    <>
      <GlobalStyles />
      <StyledErrorFallback>
        <Box>
          <Heading as="h1">Something went wrong 🤔</Heading>
          <p>{error.message || error.statusText}</p>
          <Button size="large" onClick={moveBack}>
            Try again!
          </Button>
        </Box>
      </StyledErrorFallback>
    </>
  );
}

export default ErrorFallback;
