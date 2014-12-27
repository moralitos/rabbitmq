require_relative 'rpc_client'

describe RpcClient do

  it 'should concatenate strings' do
    response = RpcClient.execute(method: 'concatenate', params: { strings: ['con', 'ca', 'te', 'na', 'tion'] })
    expect(response['status']).to eq('success')
    expect(response['params']).to be_truthy
    expect(response['params']['concatenated_string']).to eq('concatenation')
  end

  after do
    RpcClient.channel.close
    RpcClient.connection.close
  end
end
