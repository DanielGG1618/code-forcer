import { useForm } from "react-hook-form";
import Form from "../../ui/Form";
import Heading from "../../ui/Heading";
import FileInput from "../../ui/FileInput";
import Input from "../../ui/Input";
import Button from "../../ui/Button";
import FormElement from "../../ui/FormElement";
import styled from "styled-components";
import { uploadHandlesFile } from "../../api/handles";
import { useNavigation } from "react-router-dom";

const Error = styled.span`
  display: flex;
  justify-content: center;
  text-align: center;
  font-size: 1.4rem;
  color: var(--color-red-400);
`;

export default function FormFileUpdate() {
  const navigation = useNavigation();
  const {
    register,
    handleSubmit,
    watch,
    setError,
    formState: { errors },
  } = useForm();

  const watchFileInput = watch("file");

  function onSubmit({ file, link }) {
    if (file.length === 0 && link.trim().length == 0) {
      setError("neitherItem", {
        type: "manual",
        message: "You must fill out either file or link field",
      });
      return;
    }
    uploadHandlesFile(file[0]).then((res) => console.log(res));
  }

  return (
    <Form onSubmit={handleSubmit(onSubmit)}>
      <Heading as="h2">Update with a file</Heading>
      <Heading as="h3">Choose one of the options</Heading>
      <FormElement label="File from Local Storage" type="file">
        <FileInput
          edited={watchFileInput && "true"}
          text={
            watchFileInput ? watchFileInput[0]?.name : "*.csv, *.xls, *.xlsx"
          }
          accept={".csv, .xls, .xlsx"}
          register={register("file")}
        />
      </FormElement>
      <FormElement label="Link to Google Sheets">
        <Input
          disabled={navigation.state !== "idle"}
          placeholder="https://docs.google.com/spreadsheets/..."
          {...register("link")}
        />
      </FormElement>
      {errors.neitherItem && <Error>{errors?.neitherItem.message}</Error>}
      <Button as="input" type="submit" value="Submit" />
    </Form>
  );
}
