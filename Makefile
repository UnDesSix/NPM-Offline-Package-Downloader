IMAGE_NAME=npm-offline-downloader
OUTPUT_DIR=$(CURDIR)/out

all: build run

build:
	docker build -t $(IMAGE_NAME) .

run:
	mkdir -p $(OUTPUT_DIR)
	docker run --rm -v $(OUTPUT_DIR):/out $(IMAGE_NAME)

clean:
	rm -rf $(OUTPUT_DIR)

purge: clean
	docker rmi -f $(IMAGE_NAME)
