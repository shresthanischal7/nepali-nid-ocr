
from app.ocr.ocr_pipeline import OCRPipeline


def main():

    image_path = "images/sample8.jpeg"

    pipeline = OCRPipeline(image_path, engine="pdl")

    result = pipeline.process()

    print(result)


if __name__ == "__main__":
    main()
