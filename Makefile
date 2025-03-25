HEAD_SHA := $(shell git rev-parse HEAD 2>&1)

.PHONY: release
release: build
	docker push rhots/automation:$(HEAD_SHA)


.PHONY: build
build:
	docker build \
		--platform linux/amd64 \
		-t rhots/automation:$(HEAD_SHA) \
		.
