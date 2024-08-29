class SSHCommand:
    QUEUE_COUNT = "~/dpo_logs/count_queue.sh"
    DISK_USAGE = "df -h"
    DOCUMENT_COUNT = (
        "docker exec datasaur-mariadb bash -c "
        "'mysql -h$DATABASE_HOST -u$DATABASE_USERNAME -p$DATABASE_PASSWORD"
        ' -e "use datasaur; select status, count(*) from'
        " llm_vector_store_document WHERE llmVectorStoreId=9 GROUP BY status;\"'"
    )

    LIST_QUEUE = "ls /var/lib/docker/volumes/von-bot-datasaur_document-processor_backup_{source}/_data/queue_downloader"
