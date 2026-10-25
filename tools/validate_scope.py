#!/usr/bin/env python3
"""Validate the frozen source scope. This is not runtime qualification."""
import hashlib,json,pathlib
root=pathlib.Path(__file__).resolve().parents[1]
scope=json.loads((root/'repository-scope.json').read_text(encoding='utf-8'))
assert scope['outbound_effects']=='HOLD'
keys=[x['key'] for x in scope['issues']]
assert len(keys)==len(set(keys)), 'Duplicate issue key'
for item in scope['source_files']:
    path=root/item['path']
    assert path.is_file() and not path.is_symlink(), item['path']
    assert hashlib.sha256(path.read_bytes()).hexdigest()==item['sha256'], item['path']
for issue in scope['issues']:
    body=(root/issue['body_path']).read_text(encoding='utf-8')
    assert '<!-- v7-agent-package:'+issue['key']+' -->' in body
    assert hashlib.sha256(body.encode()).hexdigest()==issue['body_sha256']
print(json.dumps({'status':'PASS','scope':'SOURCE_AND_BACKLOG_ONLY','repository':scope['repository'],'issues':len(keys),'runtime_tests':'NOT_RUN','production_actions':0}))
