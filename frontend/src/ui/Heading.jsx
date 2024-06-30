import styled, { css } from "styled-components";

const Heading = styled.h1`
  line-height: 1.4;

  &:has(svg) {
    display: inline-flex;
    align-items: center;
    gap: 1.2rem;

    & svg {
      flex: 0 0 3rem;
      width: 3rem;
      height: 3rem;
      margin-bottom: 0.2rem;
    }
  }
  ${(props) =>
    props.as === "h1" &&
    css`
      font-size: 3rem;
      font-weight: 600;
      letter-spacing: 0.02em;
    `}
  ${(props) =>
    props.as === "h2" &&
    css`
      font-size: 2rem;
      font-weight: 600;
    `}
  ${(props) =>
    props.as === "h3" &&
    css`
      font-size: 2rem;
      font-weight: 500;
    `}
  ${(props) =>
    props.as === "h4" &&
    css`
      font-size: 3rem;
      font-weight: 600;
      text-align: center;
    `}
`;

Heading.defaultProps = {
  as: "h1",
};

export default Heading;
