import styled from "styled-components";

const FullPage = styled.div`
  position: absolute;
  z-index: 2;
  inset: 0;
  background-color: var(--color-grey-50);
  display: flex;
  align-items: center;
  justify-content: center;

  @media (max-width: 991.98px) {
    width: 100lvw;
    height: 100lvh;
    inset: auto;
  }
`;

export default FullPage;
