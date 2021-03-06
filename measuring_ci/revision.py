import logging

import taskcluster

log = logging.getLogger()


async def find_taskgroup_by_revision(
    revision, project, product, nightly=False,
):
    """Use the index to find a task group ID from a cset revision."""
    if nightly:
        index = (  # collapse string
            "gecko.v2.{project}.nightly.revision."
            "{revision}.{product}.linux64-opt"
        )
    else:
        index = (
            "gecko.v2.{project}.revision.{revision}.taskgraph.decision"
        )
    index = index.format(
        project=project.split('/')[-1],  # remove paths like release/ integration/
        revision=revision,
        product=product,
    )

    idx = taskcluster.aio.Index()
    queue = taskcluster.aio.Queue()

    log.debug('Looking for taskId via index {}'.format(index))
    try:
        build_task = await idx.findTask(index)
        task_def = await queue.task(build_task['taskId'])
    except taskcluster.exceptions.TaskclusterRestFailure as e:
        log.debug(e)
        return

    return task_def['taskGroupId']
