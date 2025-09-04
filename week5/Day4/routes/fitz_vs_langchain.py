from fastapi import APIRouter
from langchain_community.document_loaders import PyMuPDFLoader
import fitz

testrouter = APIRouter(prefix="/test")


@testrouter.get("/")
def test():
    try:
        file_path = "./output_Dir/Attention.pdf"

        # Raw fitz extraction for ground truth of embedded images
        fitz_doc = fitz.open(file_path)
        fitz_images_per_page = [len(p.get_images(full=True)) for p in fitz_doc]
        fitz_total_images = sum(fitz_images_per_page)

        # LangChain PyMuPDFLoader with image extraction enabled
        # Note: PyMuPDFLoader does not accept mode/images_inner_format kwargs.
        loader = PyMuPDFLoader(file_path=file_path, extract_images=True)
        docs = loader.load()

        # Inspect how images surface in LangChain docs
        meta_keys_seen = set()
        meta_images_total = 0
        content_data_uri_total = 0
        content_md_image_total = 0
        per_doc = []
        for d in docs:
            meta_image_keys = [
                k for k in d.metadata.keys() if ("image" in k.lower() or "img" in k.lower())
            ]
            meta_keys_seen.update(meta_image_keys)

            meta_count = 0
            for k in meta_image_keys:
                v = d.metadata.get(k)
                if isinstance(v, (list, tuple)):
                    meta_count += len(v)
                elif isinstance(v, dict):
                    meta_count += len(v)
                elif v is not None:
                    meta_count += 1
            meta_images_total += meta_count

            content = d.page_content or ""
            data_uri_count = content.count("data:image")
            md_img_count = content.count("![")
            content_data_uri_total += data_uri_count
            content_md_image_total += md_img_count

            per_doc.append(
                {
                    "page": d.metadata.get("page"),
                    "meta_image_keys": meta_image_keys,
                    "meta_image_count": meta_count,
                    "content_data_image_count": data_uri_count,
                    "content_md_image_count": md_img_count,
                    "content_len": len(content),
                }
            )

        return {
            "file": file_path,
            "fitz": {
                "pages": len(fitz_doc),
                "images_per_page": fitz_images_per_page,
                "total_images": fitz_total_images,
            },
            "pymupdf_loader": {
                "num_docs": len(docs),
                "meta_image_keys_seen": sorted(meta_keys_seen),
                "total_meta_images_count": meta_images_total,
                "total_content_data_uri_images": content_data_uri_total,
                "total_content_md_images": content_md_image_total,
                "per_doc": per_doc,
            },
            "note": "PyMuPDFLoader currently exposes images via metadata or content only if parser injects them; your LangChain version may not embed images in page_content. Ground truth from fitz shows actual embedded image count.",
        }
    except Exception as e:
        return {"message": "Error extracting images", "error": str(e)}