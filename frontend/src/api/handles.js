export async function uploadHandlesFile(file) {
  const url = `/students/file`;

  const response = await fetch(url, {
    method: "PUT",
    body: file,
  });

  console.log("File uploading response: ", response);

  if (!response.ok) {
    throw new Error(response.statusText);
  }

  return response;
}
export async function uploadSingleHandle(info) {
  const url = `/students/${info.email}`;

  const response = await fetch(url, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json;charset=utf-8",
    },
    body: JSON.stringify(info),
  });

  console.log("Single handle uploading response: ", response);

  if (!response.ok) {
    throw new Error(response.statusText);
  }

  return response;
}
