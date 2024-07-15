import styled, { css } from "styled-components";

const Row = styled.div`
  display: flex;
  column-gap: 1.6rem;
  row-gap: 3.5rem;

  @media (max-width: 1199.98px) {
    flex-wrap: wrap;
  }

  ${(props) =>
    props.type === "filled" &&
    css`
      & > * {
        flex: 1 1 0;
      }
      @media (max-width: 439.98px) {
        flex-direction: column;
        > * {
          flex: auto;
          width: 100%;
        }
      }
    `}
  ${(props) =>
    props.type === "splitted" &&
    css`
      align-items: center;
      justify-content: space-between;
    `}
  ${(props) =>
    props.type === "vertical" &&
    css`
      flex-direction: column;
    `}
`;

Row.defaultProps = {
  type: "horizontal",
};

export default Row;
