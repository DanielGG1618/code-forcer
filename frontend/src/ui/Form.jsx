import styled from "styled-components";

const Form = styled.form`
  max-width: 54rem;
  min-width: 32rem;
  display: flex;
  flex-direction: column;
  gap: 1.8rem;
  padding: 2.4rem 4rem;

  background-color: var(--color-grey-0);
  border: 1px solid var(--color-grey-100);
  border-radius: var(--border-radius-md);

  button[type="submit"] {
    margin-top: auto;
  }

  overflow: hidden;
  font-size: 1.4rem;

  @media (max-width: 1199.98px) {
    padding-right: 2rem;
    padding-left: 2rem;
  }
  @media (max-width: 991.98px) {
    max-width: 80%;
    margin-left: auto;
    margin-right: auto;
  }
  @media (max-width: 767.98px) {
    max-width: none;
  }
`;

Form.defaultProps = {
  type: "regular",
};

export default Form;
