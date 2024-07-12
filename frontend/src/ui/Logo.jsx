import { Link } from "react-router-dom";
import styled from "styled-components";

const StyledLogo = styled(Link)`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.05rem;

  &:hover span {
    letter-spacing: 0.08em;
  }
`;

const Img = styled.img`
  flex: 0 0 6.2rem;
  width: 6.2rem;
  height: 6.2rem;
`;
const LogoText = styled.span`
  font-weight: 500;
  font-size: 2.4rem;
  line-height: 1.2;
  letter-spacing: 0.03em;
  transition: letter-spacing 0.3s ease;
`;

function Logo() {
  return (
    <StyledLogo to="/">
      <Img src="/logo.svg" alt="The logo of out application" />
      <LogoText>CodeForcer</LogoText>
    </StyledLogo>
  );
}

export default Logo;
