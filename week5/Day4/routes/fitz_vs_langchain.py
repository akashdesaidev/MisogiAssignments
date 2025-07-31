from fastapi import APIRouter
from langchain_community.document_loaders import PyMuPDFLoader

testrouter=APIRouter(prefix="/test")

@testrouter.get("/")
def test():
    try:
        output_dir="./output_Dir/"
        file_path = "./output_Dir/Attention.pdf"
        loader = PyMuPDFLoader(
                file_path=file_path,
                mode="page",                        # Split PDF into per-page documents
                extract_images=True,                 # Enable image extraction
                images_inner_format="markdown-img"   # Embed images as markdown base64 in page content
            )

        docs = loader.load()  # docs is a list: one Document object per page

            # Fitdoc = fitz.open(filename=file_path)
            # for page_num, page in enumerate(Fitdoc):
            #  imgs = page.get_images(full=True)
            #  print(f"Page {page_num}: {len(imgs)} images")
            # Loop through docling's unified document
        return {
            "message": "Images extracted successfully (async)",          
            "note": "You can now process images_bytes asynchronously for LLM input."
        }
    except Exception as e:
        return {"message": "Error extracting images", "error": str(e)}